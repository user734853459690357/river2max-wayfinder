# What the Test Cycle data says about the cause

Type: grilling
Status: resolved
Blocked by: 08

## Question

Using the recorded Test Cycle (Prometheus) and the hypotheses in [Known causes of early cutout](02-cutout-causes.md): which cause does the data support? Look at cell min/max mV and spread approaching the Cutout, sag vs load, displayed vs BMS SoC, energy out vs 512 Wh nominal and energy back in, and full_cap/design_cap (baseline 86.4%, 275 cycles). Agree the diagnosis and how the evidence is presented (charts + numbers).

## Comments

- The monitoring stack was stopped after the run (`docker compose down`, 2026-11-12). The recorded data is kept in the `ecoflow-monitor_prometheus-data` volume. To query it, run `docker compose up -d prometheus` in `ecoflow-monitor/` (localhost:9090; range 2026-11-11 21:30 → 11-12 00:50 UTC). The exporter does not need to run.

## Answer

**Diagnosis agreed with the user on 2026-11-12.** Based on the Test Cycle data in Prometheus (2026-11-11 21:30 → 11-12 00:50 UTC).

- **Primary cause:** **Usable capacity** (see `GLOSSARY.md`) is about **11 Ah, roughly 55% of the 20 Ah design**, after only 275 cycles. The spec is "80%+ after 3000 cycles". The most likely cause is **one or more low-capacity cells** limiting the series string at both ends.
  - **Discharge, 100% → Cutout:** about 11.2 Ah. That is 281 Wh at the pack (from 8 × cell mV × A) and 275 Wh at the outputs.
  - **Recharge, 0 → full:** about 11.0 Ah. That is 298 Wh at the pack and 348 Wh at the wall.
  - **Bottom of the window:** the Cutout came with the cell average at 3.00 V under a 12 A load, and the cell average rested at 3.08 V afterwards. A uniformly empty LFP pack would rest lower.
  - **Top of the window:** charge current dropped (19 → 13 A at 00:44) with the cell average at only 3.49 V, where about 3.55–3.65 V would be expected for a full pack.
  - **Why this points to a weak cell:** the pack average is well inside LFP limits at both ends, so something other than the average is ending discharge and charge early. A low-capacity cell would do that, reaching empty first and full first. The average hides it, because min = max on this model.
- **Secondary:** the BMS gauge does not track the lost capacity. full_cap is 17.28 → 17.46 Ah (about 87%) and soh is 97, and **neither dropped after a full 0 → 100% cycle**.
  - The gauge therefore overstates the charge by about 6 Ah, which accounts for the Cutout at about 25%.
  - The Rebound happens because the gauge restores its stored 4404 mAh at every boot.
  - The Collapse to zero is the BMS's eventual reset of the gauge to zero.
  - The gauge's own corrections are visible in the data. In the last 4 minutes before the Cutout, the SoC fell 3–5× faster than the current would explain (36 → 23%). Near the top of the charge it jumped 44 → 99% in 9 minutes at a constant 19 A.
- **Ruled out as the cause:**
  - App limits ([Check the app's discharge limit and reserve settings](07-app-limits-check.md)).
  - Firmware, which is up to date.
  - Temperature: 26–35 °C during discharge.
  - Calibration drift. The BMS's own coulomb count saw only about 11 Ah in each direction, and the Test Cycle already was an EcoFlow-style calibration cycle (drain until it shuts itself off, then an uninterrupted AC charge), yet full_cap did not drop.
- **Side note:** the cell temperature reached **46 °C** at the end of the AC charge, at the manual's 45 °C charge limit.
- **Accepted limitation:** without per-cell data, "weak cell" cannot be told apart from whole-pack fade. We will not investigate further (opening the unit would void the warranty). Both readings put capacity far outside spec, so the evidence will say **"low-capacity cell suspected; per-cell confirmation is EcoFlow's"**.
- **How the evidence is presented:** static PNG charts generated from Prometheus, plus a one-page summary table. They will be built when the evidence package is assembled, not as part of this ticket.
  1. Full discharge: SoC, cell average and current.
  2. Cutout close-up: the accelerating SoC drop and the Rebound.
  3. Recharge: the 44 → 99% jump.
  4. Capacity bar: design 20 Ah vs BMS 17.5 Ah vs measured about 11 Ah.

  Grafana screenshots were rejected because they are harder to annotate and reproduce.
