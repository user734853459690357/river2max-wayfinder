# River 2 Max cutout diagnosis

Status: complete (2026-11-13). Destination reached: the diagnosis is in [What the Test Cycle data says about the cause](issues/09-diagnose-from-data.md), and the next action, a warranty claim through the dealer, has its evidence in the Fault report.

Label: wayfinder:map

## Destination

A diagnosis of why the River 2 Max has a **Cutout** at ~25% Displayed SoC (see `GLOSSARY.md`), backed by data from a monitored **Test Cycle**, plus the next action (setting change, recalibration, or warranty claim with evidence).

## Notes

- Domain: consumer LiFePO4 power station (EcoFlow River 2 Max) + monitoring stack from https://github.com/tess1o/go-ecoflow-exporter.
- Vocabulary: use `GLOSSARY.md` terms (Displayed SoC, Cutout, Rebound, Collapse to zero, Runtime, Test Cycle).
- **Execution override:** this map carries execution of the monitoring setup (installing and running the exporter stack) — it is a means to the diagnosis — and drafting the warranty evidence package for user review.
- Host: this WSL laptop, running the exporter's docker-compose plus Prometheus + Grafana we add ourselves (v2.0.0 compose ships the exporter only) for a supervised Test Cycle of a few hours, not 24/7.
- Analysis happens here: query Prometheus directly from the session; Grafana is for the user's eyes.
- Symptoms so far: Cutout under load at ~25% (~20% at 200 W+); Rebound to 33/47% after; idle runs fine at "25%"; re-loading after Rebound → Collapse to zero; recharges from Cutout value to 100%; Runtime fell from 3.5–4 h to ~2.5 h.
- Preference: research facts via research tickets, grill only for decisions.
- Research findings are saved under `research/` in this folder (not on `research/<name>` branches). Credentials (email, password, serial) live in `ecoflow-monitor/.env`, which is git-ignored; the recorded Test Cycle data lives in the Docker volume `ecoflow-monitor_prometheus-data`, not in git.

## Decisions so far

- [Is this laptop ready to record a Test Cycle](issues/03-laptop-readiness.md): yes. Docker Desktop and EcoFlow cloud (HTTPS + MQTT 8883) both work. Windows sleeps after 5 min, so run `tools/keep-awake.ps1`, stay on AC, and keep the lid open.
- [What the exporter collects for a River 2 Max](issues/01-exporter-capabilities.md): min/max cell mV, current, temps, BMS vs Displayed SoC, capacities via MQTT (account login); no per-cell array; v2.0.0 compose ships exporter only.
- [Known causes of early cutout on River 2 Max / LFP packs](issues/02-cutout-causes.md): leading hypothesis is a weak or imbalanced cell (voltage-triggered cutoff); rule out the app discharge limit first; key signals are cell mV spread, sag vs load, Wh out vs 512 Wh.
- [Check the app's discharge limit and reserve settings](issues/07-app-limits-check.md): limits always 0–100%, firmware up to date; app limits ruled out.
- [How to log in to EcoFlow and get the data](issues/04-data-access-method.md): account-login MQTT (`EXPORTER_TYPE=mqtt`) on the main account; credentials in `ecoflow-monitor/` in the project folder (`.env` + password file, chmod 600), with the password typed by the user; if login fails, stop and regrill.
- [Install and verify the monitoring setup](issues/05-install-stack.md): running in `ecoflow-monitor/`, Grafana at localhost:3000. The unit only answers polls, so snapshots are requested every 10 s. Negative current means discharge. Baseline: 275 cycles, full cap 86.4% of design, cell spread 0 mV.
- [How to run the Test Cycle](issues/06-test-cycle-protocol.md): start from 100%, laptop as the normal-use load (~40–90 W), user posts timed notes at Cutout/Rebound, tries Collapse to zero, then uninterrupted AC recharge to 100%.
- [Run the Test Cycle](issues/08-run-test-cycle.md): recorded 2026-11-11 21:30 → 11-12 00:50 UTC. Cutout at 23–25% with cells at 3.0 V under load; ~275 Wh out of a rated 512; Collapse to zero at 3.08 V rest; 348 Wh in at the AC socket; SoC jumped 44→99% near the top of charge.
- [What the Test Cycle data says about the cause](issues/09-diagnose-from-data.md): Usable capacity is about 11 Ah (~55% of design) at 275 cycles. A low-capacity cell is suspected, and the BMS gauge still assumes about 17.4 Ah. Calibration drift, settings and temperature are ruled out. Evidence will be PNG charts plus a summary table.
- [Calibrate first or claim the warranty now](issues/10-calibrate-or-claim.md): claim now through the authorized dealer (shipping details already received), because 5+ calibration cycles did not help. The claim pre-empts "normal wear" with the spec. Evidence goes in a factual owner's Fault report with no AI mentions, printed in the box and emailed to the dealer.
- [What goes in the warranty evidence package](issues/11-evidence-package.md): the Fault report alone, in English and Ukrainian, finished and ready to send. Dealer copies with the full serial are kept local; the repo has copies with the serial masked.

## Not yet specified

- (none: map complete, all tickets resolved)

## Out of scope
