# What the exporter collects for a River 2 Max

Type: research
Status: resolved
Blocked by:

## Question

For a River 2 Max, what does go-ecoflow-exporter (https://github.com/tess1o/go-ecoflow-exporter) actually collect, and how? Specifically: which metrics (pack voltage, current, per-cell voltages, temperatures, BMS SoC vs displayed SoC, design/full capacity, cycles, output watts), at what sample rate, and via which access method (EcoFlow developer REST API access/secret keys vs account-login MQTT) — with the trade-offs and setup prerequisites of each. Include how the docker-compose stack is launched.

## Comments

- Findings: `research/01-exporter-capabilities.md` (.scratch/river2max-cutout/research/01-exporter-capabilities.md)

## Answer

Findings: [research/01-exporter-capabilities.md](../research/01-exporter-capabilities.md).
- No per-cell voltages: only min/max cell voltage (mV). The pack voltage is in whole volts, too coarse to show sag.
- Available: pack current, temperatures, BMS SoC vs Displayed SoC, design/full/remaining capacity (mAh), cycles, output watts, discharge-limit setting (`minDsgSoc`), fault fields.
- MQTT (account login) is the access path with BMS detail. Its effective sample rate is the Prometheus scrape_interval (suggested about 5 s). REST (developer keys) is unconfirmed for BMS fields and polls every 30 s by default.
- Exporter v2.0.0's docker-compose runs only the exporter (port 2112). Prometheus and Grafana must be added by us (template: tag 1.8.0); the dashboard JSON can be imported.
- Still to check on a live `/metrics`: the sign of the current reading and the device's push rate.
