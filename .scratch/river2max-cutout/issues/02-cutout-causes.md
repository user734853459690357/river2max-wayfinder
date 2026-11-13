# Known causes of early cutout on River 2 Max / LFP packs

Type: research
Status: resolved
Blocked by:

## Question

What are the known causes of a River 2 Max (LiFePO4) powering off under load at ~20–25% displayed SoC, with Rebound after and Collapse to zero on re-load, and Runtime dropping from 3.5–4 h to ~2.5 h? Cover: app discharge-limit settings, BMS SoC calibration drift on LFP, cell imbalance / weak cell, capacity fade, firmware issues, and EcoFlow's recommended calibration procedure. For each cause: which measurable signals (pack/cell voltage under load, cell delta, temperature, full-capacity vs design capacity) would distinguish it. Also: what EcoFlow warranty/support expects as evidence.

## Comments

- Findings: `../research/02-cutout-causes.md`

## Answer

Findings: [research/02-cutout-causes.md](../research/02-cutout-causes.md).
- Leading hypothesis: a weak or imbalanced cell, or high internal resistance. The symptoms point to a voltage-triggered cutoff (load-dependent, with Rebound and Collapse to zero), not a percentage threshold. SoC calibration drift alone cannot explain the ~30–35% Runtime loss.
- Rule out first: the app's Min Discharge Level (0–30%, `minDsgSoc`) and Backup Reserve. A set limit would cut out at the same percentage regardless of load and show no Rebound.
- Signals that tell the causes apart: min/max cell mV spread at the Cutout, voltage sag at 50 W vs 200 W, Wh out vs 512 Wh nominal, Wh in on recharge, fullCap/designCap, soh, cycles, temperature.
- Calibration (EcoFlow general guidance): set limits to 0%, discharge until the unit shuts off, rest 1–2 h, charge on AC to 100% without interruption, repeat 1–3 times.
- Warranty: 5 years, mail-in, needs serial number and proof of purchase. "Normal wear" is excluded, with no published capacity threshold. The spec reference is 80%+ capacity after 3000 cycles.
