# EcoFlow River 2 Max: diagnosing an early shutdown with Wayfinder

This repo had two goals:

1. **Try out the [wayfinder](.claude/skills/wayfinder/SKILL.md) skill.** Wayfinder breaks a vague, multi-session problem into a map of decision tickets, then works through them one at a time with an AI coding agent.
2. **Diagnose a real fault.** An EcoFlow River 2 Max power station switched itself off at about 25 % displayed charge, and its runtime had dropped from 3.5–4 h to about 2.5 h.

## Outcome

[Fault report](.scratch/river2max-cutout/evidence/package/fault-report.pdf)

## How the map went

The map is [`.scratch/river2max-cutout/map.md`](.scratch/river2max-cutout/map.md). Each ticket under [`issues/`](.scratch/river2max-cutout/issues/) holds its question and the answer that resolved it:

| # | Ticket | Type |
|---|---|---|
| 01 | What the exporter collects for a River 2 Max | research |
| 02 | Known causes of early cutout on River 2 Max / LFP packs | research |
| 03 | Is this laptop ready to record a Test Cycle | task |
| 04 | How to log in to EcoFlow and get the data | grilling |
| 05 | Install and verify the monitoring setup | task |
| 06 | How to run the Test Cycle | grilling |
| 07 | Check the app's discharge limit and reserve settings | task |
| 08 | Run the Test Cycle | task |
| 09 | What the Test Cycle data says about the cause | grilling |
| 10 | Calibrate first or claim the warranty now | grilling |
| 11 | What goes in the warranty evidence package | prototype |

The domain vocabulary (Cutout, Rebound, Collapse to zero, Usable capacity, …) is defined in [`GLOSSARY.md`](GLOSSARY.md).

## Repo layout

| Path | What it is |
|---|---|
| `ecoflow-monitor/` | Docker Compose stack: [go-ecoflow-exporter](https://github.com/tess1o/go-ecoflow-exporter) (account-login MQTT), Prometheus and Grafana with a Test Cycle dashboard |
| `.scratch/river2max-cutout/` | The wayfinder map, its tickets and the research notes |
| `.scratch/river2max-cutout/evidence/` | Fault report templates, the chart script, and the generated example reports |
| `.claude/skills/` | Agent skills used in this repo |
| `docs/agents/` | How the skills map onto this repo (local-markdown issue tracker, labels, domain docs) |

## Running the monitor

```sh
cd ecoflow-monitor
cp .env.example .env && chmod 600 .env   # EcoFlow account email, password, device serial
docker compose up -d                     # Grafana: http://localhost:3000
```
