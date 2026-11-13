# Install and verify the monitoring setup

Type: task
Status: resolved
Blocked by: 03, 04

## Question

Bring up the go-ecoflow-exporter (v2.0.0 compose runs the exporter only) plus Prometheus (short scrape_interval, ~5 s) and Grafana with the repo's dashboard imported on this laptop with the chosen access method (account-login MQTT, stack and credentials in `ecoflow-monitor/` in the project folder per [How to log in to EcoFlow and get the data](04-data-access-method.md); the user types the password), and verify the River 2 Max's metrics land in Prometheus and appear in Grafana at the expected sample rate. Also confirm the current-sign convention and the device's real push rate on /metrics. Record URLs, credential location, and the list of metric names actually available.

## Answer

**Done and verified, 2026-11-11.** The stack is running and River 2 Max data is arriving.

- **Where:** `ecoflow-monitor/` in the project folder. `compose.yml` runs the exporter `tess1o/go-ecoflow-exporter:2.0.0`, Prometheus `v3.5.0` (5 s scrape, 90 d retention) and Grafana `12.1.0`. Start with `docker compose up -d` and stop with `docker compose down`; data stays in named volumes.
- **URLs (bound to localhost only):**
  - Grafana: http://localhost:3000. No login. The home dashboard is **River 2 Max — Test Cycle**, provisioned from `grafana/dashboards/river2max.json`.
  - Prometheus: http://localhost:9090
  - Exporter: http://localhost:2112/metrics
- **Credentials:** `ecoflow-monitor/.env` (email, serial) and `ecoflow-monitor/secrets/ecoflow_password` (entered by the user with `set-password.sh`), both chmod 600. The exporter runs as uid 1000 so it can read them. MQTT login worked on the first try.
- **Sample rate:** the unit pushes **nothing unprompted**. With the default settings we saw 0 messages/min, so data refreshed only every 5 min. The fix is `MQTT_STATE_REFRESH_INTERVAL_SECONDS=10`, which gives about 12–17 full snapshots/min; Prometheus stores a sample every 5 s. Watch `rate(ecoflow_exporter_mqtt_messages_total[1m])` on the dashboard.
- **Current sign:** `ecoflow_bms_bms_status_amp` = −2 while discharging about 56–59 W on USB-C with no input, so **negative means discharge**. It is whole amps (coarse), and `bms_status_vol` is whole volts. For a finer sag signal use `8 × min_cell_vol` (8S LFP: 25.96 V shown while `vol` = 25). `mppt_out_vol` sat at 26052 and never changed, so don't use it.
- **Metric names:** 151 distinct names exported. The list is in [research/05-metric-names.txt](../research/05-metric-names.txt). The key signals are on the dashboard: displayed SoC vs BMS SoC, min/max cell mV and spread, power in/out, current/voltage, remaining/full/design capacity, temperatures, and fault/protection flags.
- **Baseline readings (at about 91% Displayed SoC, idle-ish):**
  - cycles **275**
  - full_cap / design_cap = 17280 / 20000 mAh = **86.4%**; `soh` reports 97
  - cell spread 0 mV (3245 mV)
  - `min_dsg_soc` 0, `max_charge_soc` 100
  - `pd_bp_power_soc` 80 (backup-reserve level field; `pd_watch_is_config` 0)
  - all fault fields 0
- **Caveats for the Test Cycle:**
  - After 5 min of silence (`MQTT_DEVICE_OFFLINE_THRESHOLD_SECONDS`) the exporter drops the series. Prometheus history is kept.
  - The last sample before a Cutout is at most about 10 s old, so the final seconds may be missed.
  - Laptop sleep is still handled per [Is this laptop ready to record a Test Cycle](03-laptop-readiness.md).
