# What go-ecoflow-exporter collects for a River 2 Max

Answers ticket `issues/01-exporter-capabilities.md`. Researched 2026-11-11.

Sources read:
- go-ecoflow-exporter at tag `2.0.0` (commit `4cb2418`, 2026-10-20): README, `docker-compose.yml`, `config.go`, `metric.go`, `prometheus.go`, `rest_exporter.go`, `mqtt_exporter.go`, `telemetry.go`, plus tag `1.8.0` for the old compose stack.
- go-ecoflow library v1.1.0 (`client.go`, `mqtt_client.go`, `mqtt_model.go`, `docs/fields_mapping_delta_2.md`), which the exporter uses for all EcoFlow I/O.
- The EcoFlow developer portal's own JS bundle (`cdn-fe.ecoflow.com/ef-open-platform/static/js/main.8c3abe3b.js` and the River 2 Pro doc chunk `6751.cba601fe.chunk.js`). The portal is a single-page app, so this bundle is the only machine-readable copy of the official docs.
- tolwi/hassio-ecoflow-cloud (commit `7dcf951`, 2026-11-03): `diag/river_2_max.json`, a real River 2 Max parameter dump captured over app-login MQTT, plus `devices/registry.py` and `devices/internal/river2_max.py`. This is the best available evidence for what a River 2 Max actually sends. It is a third-party capture, not EcoFlow documentation.

## Short answer

- **The exporter exports every numeric field the device sends, with no per-model list.** For example, `bms_bmsStatus.minCellVol` becomes the metric `ecoflow_bms_bms_status_min_cell_vol{device,serial_number}`. Strings and arrays are dropped, and booleans become 0/1. Sources: README "Metrics"; `metric.go` `ecoflowParamToPrometheusMetric` and `toFloat`; `prometheus.go` `Handle`.
- **Use MQTT mode (account email and password) for a River 2 Max.** It is the only mode with full BMS detail, and the official developer (REST) API does not document the River 2 Max at all. See "Access methods".
- **The River 2 Max reports no per-cell voltages, only the minimum and maximum cell voltage (mV).** It does report BMS SoC, displayed SoC, design, full and remaining capacity, cycles, current, temperatures and output watts.
- **The v2 `docker-compose.yml` starts only the exporter.** Prometheus and Grafana are not included and have to be added separately.

## Fields a River 2 Max reports over app-login MQTT

These field names come from the hassio-ecoflow-cloud dump `diag/river_2_max.json`, which is keyed exactly as the app-MQTT `params` arrive. That project feeds `params` straight in (`devices/__init__.py` `_prepare_data`), just as the exporter does (`mqtt_exporter.go` `MessageHandler` → `deviceParams.Params`). The value in parentheses is from that one capture. Units come from go-ecoflow's Delta 2 field map unless noted otherwise. The Delta 2 is a sibling model with the same field names.

| Need | Field → exported metric | Notes |
|---|---|---|
| Pack voltage | `bms_bmsStatus.vol` → `ecoflow_bms_bms_status_vol` (26) | Delta 2 docs say mV, but the River 2 Max sent `26`, and hassio's `river2_max.py` treats it as **volts** (`VoltSensorEntity`). **Probably integer volts, so 1 V resolution, which is too coarse.** `mppt.outVol` (26116) looks like a mV voltage near the pack voltage, but this is unverified. |
| Pack current | `bms_bmsStatus.amp` → `..._bms_status_amp` (0) | mA (Delta 2 docs). Also `bms_emsStatus.chgAmp`, `inv.invOutAmp`, `inv.acInAmp`. |
| Cell voltages | `bms_bmsStatus.minCellVol`, `maxCellVol` (3254 / 3254) | mV. **No per-cell array is reported.** The min–max spread is the only imbalance signal. |
| Temperatures | `bms_bmsStatus.temp`, `minCellTemp`, `maxCellTemp`, `minMosTemp`, `maxMosTemp`; `inv.outTemp`, `mppt.carTemp` | °C |
| BMS SoC | `bms_bmsStatus.soc` (36), `bms_bmsStatus.f32ShowSoc` (35) | |
| Displayed SoC | `bms_emsStatus.lcdShowSoc` (36), `bms_emsStatus.f32LcdShowSoc` (35), `pd.soc` (36) | Delta 2 docs: "SoC value displayed on LCD"; `pd.soc` = "Display SOC". |
| Capacity | `bms_bmsStatus.designCap` (20000), `fullCap` (17978), `remainCap` (6385) | mAh. In that capture, fullCap/designCap ≈ 90%. |
| Health | `bms_bmsStatus.soh` (0), `bms_bmsStatus.cycles` (11) | `soh` read 0 in the capture, so it may not be populated on this model. Compute fullCap/designCap instead. |
| Output watts | `pd.wattsOutSum`, `inv.outputWatts`, `bms_bmsStatus.outputWatts`, plus per-port `pd.usb1Watts`, `pd.typec1Watts`, `pd.carWatts`, … | W |
| Input watts | `pd.wattsInSum`, `inv.inputWatts`, `mppt.inWatts`, `bms_bmsStatus.inputWatts` | W |
| Protection and limits | `bms_bmsStatus.bmsFault`, `errCode`, `bqSysStatReg`, `bms_emsStatus.bmsWarState`, `dsgCmd`, `chgCmd`, `minDsgSoc`, `maxChargeSoc`, `pd.minAcoutSoc`, `inv.errCode` | Likely useful around a Cutout. `bqSysStatReg` is the "BQ hardware protection register" (Delta 2 docs). |
| Time estimates | `bms_emsStatus.dsgRemainTime`, `chgRemainTime`, `pd.remainTime` | minutes; 5999 = idle |

The bundled Grafana dashboard (`grafana_dashboards/ecoflow-prometheus.json`) mostly queries `bms_master_*` and `bms_slave_*`, which are Delta Max/Pro-style names. On a River 2 Max most of its panels will be empty. Only a few, such as `bms_bms_status_vol`, `inv_output_watts` and `pd_watts_in_sum`, match. Expect to build your own panels.

## Sample rate

- **MQTT mode:** updates arrive when the device sends them, with no fixed rate. The exporter merges each message into a cached full state per device (`mqtt_exporter.go`). Every 20 s (`MQTT_PING_INTERVAL_SECONDS`) it sends a `setRtcTime` keep-alive, and every 300 s (`MQTT_STATE_REFRESH_INTERVAL_SECONDS`) it sends `latestQuotas` to make the device keep publishing. **No primary source states how often a River 2 Max sends data** (unverified; community reports suggest every few seconds). Measure it during the test with `ecoflow_exporter_mqtt_messages_total` and `ecoflow_exporter_last_message_timestamp_seconds` (`telemetry.go`).
- **REST mode:** the API is polled every `SCRAPING_INTERVAL` = 30 s by default (`config.go` `defaultRestIntervalSeconds`; `rest_exporter.go`). The interval is configurable, and the EcoFlow rate limits are not documented in the sources read.
- **Either mode:** Prometheus stores only the latest value at each scrape (`prometheus.go` gauges). The effective resolution is therefore the slower of the device or API rate and the Prometheus `scrape_interval`. The old v1 stack used 30 s (`1.8.0/docker-compose/prometheus/prometheus.yml`). To catch the lead-up to a Cutout, set the scrape interval to about 5 s.
- **During a Cutout:** after `MQTT_DEVICE_OFFLINE_THRESHOLD_SECONDS` (300 s) of silence, every parameter series for the device is deleted and `ecoflow_online` drops to 0. Readings stop at the last value received before the shutdown, so the final seconds before a Cutout may never be sent.

## Access methods

| | MQTT (app login) | REST (developer API) |
|---|---|---|
| Credentials | EcoFlow app email and password, plus device serial numbers in `ECOFLOW_DEVICES` (required) | `ECOFLOW_ACCESS_KEY` / `ECOFLOW_SECRET_KEY` from the developer portal |
| How it works | `POST api.ecoflow.com/auth/login` → `/iot-auth/app/certification` for broker credentials. The exporter then subscribes to `/app/device/property/<SN>` and publishes keep-alives to `/app/<userId>/<SN>/thing/property/{set,get}` (go-ecoflow `mqtt_client.go`; exporter `mqtt_exporter.go`) | Signed `GET /iot-open/sign/device/list` and `/iot-open/sign/device/quota/all` (go-ecoflow `client.go`) |
| River 2 Max fields | The full internal set above | **Not documented.** The official portal includes docs for River 2 **Pro**, Delta 2, Delta 2 Max and others, but has no River 2 or River 2 Max page. Its asset list contains no River 2/2 Max file. The River 2 Pro REST doc lists only about 20 quota fields: watts, `pd.soc`, `bms_bmsStatus.remainTime`, SoC limits and AC config, with **no voltages, cell data, temperatures, capacity or cycles**. hassio-ecoflow-cloud has the River 2 Max public-API mapping commented out (`registry.py`). |
| Prerequisites | None beyond the app account. The password is stored in the compose environment (or use `ECOFLOW_PASSWORD_FILE`). | Apply with "Become a Developer" on developer-eu.ecoflow.com, then wait for an approval email (wait time not stated) before keys can be created |
| Trade-offs | Unofficial and reverse-engineered, and can break if EcoFlow changes things. README notes the broker sometimes stops delivering data after the phone app is opened and closed; the exporter forces a reconnect or re-login. | Official and stable, but slow to get access, polled at 30 s, and for a River 2 Max it might return nothing or only a small field set |

If both sets of credentials are present, the exporter uses REST (`config.go` `detectExporterType`). For MQTT, leave the access and secret keys empty, or set `EXPORTER_TYPE=mqtt`.

## Launching the stack

The v2 `docker-compose.yml` defines one service, `tess1o/go-ecoflow-exporter:2`, on port 2112:

1. Fill in `ECOFLOW_EMAIL`, `ECOFLOW_PASSWORD` and `ECOFLOW_DEVICES` (the River 2 Max serial) in the compose file.
2. Run `docker compose up -d`.
3. Check that `http://localhost:2112/metrics` and `/healthz` respond.
4. **Run Prometheus and Grafana yourself.** v2 removed the old `docker-compose/` folder, which held the Prometheus, Grafana and Alertmanager files (README "Upgrading from v1"). Add a scrape job targeting `<host>:2112`, then import `grafana_dashboards/ecoflow-prometheus.json`. You can adapt the v1 files at tag `1.8.0` (`prometheus-compose.yml`, `grafana-compose.yml`, `prometheus/prometheus.yml`).

The exporter makes outbound HTTPS and MQTT connections to EcoFlow's cloud. The River 2 Max must be on Wi-Fi and online in the EcoFlow app.

## Uncertainties

- The River 2 Max field list comes from one third-party capture with firmware `sysVer 33620311`. A different firmware version could add or drop fields.
- `bms_bmsStatus.vol` being whole volts on a River 2 Max is inferred from that capture and hassio's unit choice, not from EcoFlow documentation.
- Whether REST `quota/all` returns anything for a River 2 Max was not tested. "Not documented" does not prove "not supported".
- The MQTT update rate was not measured.
