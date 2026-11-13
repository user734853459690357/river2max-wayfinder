# Research: known causes of early Cutout on River 2 Max (LFP)

Ticket: `../issues/02-cutout-causes.md`. Terms follow `GLOSSARY.md` (Displayed SoC, Cutout, Rebound, Collapse to zero, Runtime, Test Cycle).
Researched 2026-11-11.

## TL;DR

- **The key inference: miscalibration on its own cannot cost Runtime.** If the Displayed SoC were only *wrong*, the pack would still deliver its full energy, and only the percentage at the Cutout would be off. A drop from 3.5–4 h to ~2.5 h (about 30–35% less energy) means energy is actually missing. Either the pack has really faded, or energy is being left behind because something trips under-voltage protection early: a weak or imbalanced cell, or high internal resistance. SoC drift can sit on top of either. (This is inference from [BU-903] and [BU-803a], not an EcoFlow statement.)
- **Load-dependent Cutout + Rebound + Collapse to zero is the textbook signature of a voltage-triggered cutoff, not an SoC-threshold one.** Under load the weakest cell (or the whole pack, if internal resistance is high) sags below the BMS under-voltage limit. After the trip the voltage relaxes, so the rested reading looks healthier (Rebound). Re-loading trips it again, and the BMS then snaps its gauge to its "empty" anchor (Collapse to zero). Sources: [BU-803a], [BU-903], and analogous reports in [Bluetti-AC200Max] (secondary).
- **The cheapest check is the app settings.** The River 2 Max has a *Min Discharge Level* of 0–30% and a *Backup Reserve*, so 25% is within range. But a limit set there would act at a fixed SoC whatever the load, light LCD icon 9, and would not give a Rebound or Collapse to zero. The symptoms argue against it, yet it still has to be ruled out first, and set to 0% before any calibration.
- **The decisive Test Cycle signals** are min and max cell voltage, and their difference, at and just before the Cutout; cell temperature; Wh out from 100% to the Cutout versus 512 Wh nominal; Wh in on the recharge; and the BMS fields `fullCap`/`designCap`/`soh`/`cycles`.
- **I found no official River 2 Max calibration procedure.** EcoFlow's general guidance is to drain under load until the unit shuts itself off at 0%, optionally rest, then charge uninterrupted on AC to 100%, repeated 1–3 times. The warranty is 5 years. EcoFlow asks only for the serial number and proof of purchase or delivery, publishes no capacity threshold, and excludes "normal wear and tear" of batteries.

## Unit facts (official manual)

From the EcoFlow RIVER 2 Max User Manual V1.0 (model EFR610) [Manual]:

- Capacity: **512 Wh (20 Ah, 25.6 V)**, which implies 8 LFP cells in series. Cell material: LFP. Cycle life: **"80%+ capacity after 3000 cycles"**.
- AC output: 500 W rated (1000 W peak). With X-Boost it runs devices rated up to 1000 W by lowering voltage.
- Temperatures:

  | Use | Range |
  |---|---|
  | Discharge | −10 °C to 45 °C |
  | Charge | 0 °C to 45 °C |
  | Optimal | 20 °C to 30 °C |

  The safety section says at low temperature "the product performance may be severely reduced, or the product may cease to work."
- LCD icon 9 is **"Discharge/Recharge level limitation"**. Icons 14 and 15 are the low-temperature and overload warnings. The troubleshooting table lists flashing indicators for battery discharge low or high temperature, AC overload, and others. None of the documented warnings corresponds to "low SoC".
- Care: "For long-term storage, please recharge the product every three months (firstly discharge it to 0%, then recharge it to 60%). The product will not be covered by the warranty if it is not charged or discharged for more than 6 months." After long idle periods at very low charge the unit enters "deep sleep protection mode".
- The manual contains **no SoC-calibration procedure** and no FAQ about early shutdown.

## App and BMS fields the River 2 Max exposes

Source: the hassio-ecoflow-cloud River 2 Max device doc [HA-R2Max]. It is community-maintained, not EcoFlow documentation. The fields are useful for the Test Cycle, and ticket 01 should confirm which of them go-ecoflow-exporter actually exports.

| Purpose | Fields |
|---|---|
| Displayed vs BMS SoC | `bms_emsStatus.lcdShowSoc` (displayed), `bms_bmsStatus.soc` (BMS) |
| Pack voltage and cells | `bms_bmsStatus.vol`, `minCellVol`, `maxCellVol`, `minCellTemp`, `maxCellTemp`, `temp` |
| Health and capacity | `designCap`, `fullCap`, `remainCap`, `soh`, `cycles` |
| Power | `pd.wattsOutSum`, `pd.wattsInSum`, `inv.inputWatts`, `inv.outputWatts`, `inv.outTemp` |
| Settings | `bms_emsStatus.minDsgSoc` (**Min Discharge Level, 0–30**), `bms_emsStatus.maxChargeSoc` (50–100), `pd.watchIsConfig` / `pd.bpPowerSoc` (Backup Reserve, 5–100), `mppt.powStandbyMin` (Unit Timeout), `mppt.acStandbyMins` (AC Timeout), `mppt.cfgAcXboost` |

The doc lists **no pack current sensor**, so energy has to be estimated from watts.

## Candidate causes and distinguishing signals

LFP background, which all the causes below rely on:

- LFP has "a very flat discharge profile, making voltage estimations for SoC estimation difficult" [BU-903]. SoC is mainly coulomb counting, which drifts and needs periodic calibration to bring the "digital battery" back in line with the "chemical battery" [BU-903].
- A loaded voltage "falsifies voltage-based SoC measurement". A rested voltage needs about 4 h of open circuit to be meaningful [BU-903].
- In a series string, "the weak cell holds less capacity and is discharged more quickly", and protection must disconnect when the weakest cell reaches its floor (BU cites ~2.80 V per cell). Cells drift apart "with use and time" [BU-803a].
- Typical LFP cell floors are 2.5 V absolute and ~2.8–3.0 V as a practical BMS floor. Internal resistance and voltage sag rise steeply at low SoC. These numbers are from vendor and secondary sources [LFP-sag], and EcoFlow does not publish the River 2 Max's cutoff voltages.

### 1. App discharge-limit or reserve settings

**Mechanism:** Min Discharge Level (0–30%) or Backup Reserve stops discharge at a set SoC. Timeouts switch off by time, not SoC.

**Signals that point to it:**
- `minDsgSoc` (or `bpPowerSoc` with reserve enabled) is set at about 20–25%.
- The Cutout happens at the same Displayed SoC whatever the load.
- LCD icon 9 is lit [Manual].
- Cell voltages are still on the plateau, about 3.2 V per cell, at the Cutout.
- There is no Rebound or Collapse to zero.
- In sibling manuals, reaching the limit disables AC and 12 V output rather than dropping the screen [DELTA Pro 3 / RIVER 3 Plus manual snippets, via search; secondary].

**Signals against it:** the Cutout is load-dependent (25% vs 20%), and there is a Rebound and a Collapse to zero.

**Verdict:** unlikely, but rule it out first because it costs nothing.

### 2. BMS SoC calibration drift (coulomb-count error, stale full-capacity estimate)

**Mechanism:** the gauge loses its true full and empty anchors [EF-NotFull] [EF-Recal] [BU-903].

**Signals that point to it:**
- At the Cutout, *all* cells are genuinely low together: `minCellVol` ≈ `maxCellVol`, both at the knee, with a small delta.
- Wh delivered from 100% to the Cutout matches `fullCap` and the recharge Wh.
- The percentage at the Cutout moves toward 0% after 1–3 full calibration cycles.

**Signals against it:** drift *alone does not reduce Runtime*. The energy delivered stays the same and only the label is wrong.

**Verdict:** likely a *contributing* factor, since it explains the odd percentages, but not the primary cause of the lost Runtime.

### 3. Weak cell or cell imbalance (low capacity or high internal resistance in one cell)

**Mechanism:** one cell hits under-voltage while the others still hold charge [BU-803a].

**Signals that point to it:**
- **The cell delta (`maxCellVol − minCellVol`) widens sharply in the last part of the discharge and under higher load.** The minimum cell sits at about 2.5–2.8 V while the maximum is still about 3.1–3.2 V.
- Pack voltage is not uniformly collapsed.
- After the Cutout, the minimum cell recovers more slowly or rests lower than the others.
- A large delta at the top of charge as well suggests imbalance.
- The symptoms persist after calibration cycles.
- EcoFlow's own blog treats a cell gap of about 0.1 V or more as a sign of balancing problems [EF-BMS].

**Signals against it:** a delta that stays small through the Cutout.

**Verdict:** a leading candidate. It fits the load dependence, Rebound, Collapse to zero, and lost Runtime. It is a hardware fault and therefore a warranty case.

### 4. Capacity fade or high internal resistance across the whole pack (ageing)

**Mechanism:** the whole pack holds less energy, or sags uniformly more under load.

**Signals that point to it:**
- `fullCap/designCap` or `soh` is well below 100%.
- `cycles` is high. LFP is rated 80%+ after 3000 cycles [Manual], so ~65–70% effective capacity at a low cycle count would be abnormal.
- The cell delta stays small while all cells sag together under load.
- Wh delivered is much higher at a low load than at a high load, which shows internal resistance.
- Wh in on recharge is also low.

**Signals against it:** `soh` near 100% and a low cycle count.

**Verdict:** possible. Check `cycles` and `soh`. If they are abnormal at low cycles, that is a warranty argument, but "normal wear" is excluded.

### 5. Temperature or loading conditions

**Mechanism:** cold raises internal resistance and cuts deliverable capacity. Over-temperature or overload trips protection [Manual].

**Signals that point to it:**
- `minCellTemp` is below about 10 °C, or outside −10 °C to 45 °C.
- The low or high temperature or overload icons are shown.
- The behaviour varies with ambient temperature.

**Signals against it:** cell temperature at 20–30 °C, and no warning icons. Note that 200 W at about 25.6 V is only about 8 A (~0.4 C), which should not sag a healthy pack.

**Verdict:** a control variable for the Test Cycle. Record the temperature.

### 6. Firmware

**Mechanism:** an SoC algorithm or protection bug, or calibration that a firmware update resets.

**Signals that point to it:**
- The behaviour changed after an update.
- An update changes it.
- Other units on the same version report the same behaviour.

**Signals against it:** hard to prove. **No River 2 Max-specific known issue was found.** EcoFlow generally advises updating via the app (the RIVER 3 Plus example) [EF-NotFull] [EF-BMS].

**Verdict:** low prior. Record the firmware version and update it before the Test Cycle.

### Derived discriminators for the Test Cycle

**1. Energy budget.**
- A healthy unit should deliver roughly 512 Wh × inverter efficiency, which is very roughly 400–460 Wh at AC. *That efficiency range is an assumption, not an EcoFlow figure.*
- 3.75 h × 0.75 ≈ 2.8 h, so losing the bottom ~25% alone explains most of the Runtime drop. Compare the Wh out to the Cutout with the Wh in on the recharge and with `fullCap`.

**2. Cell delta trace.** Plot `maxCellVol − minCellVol` and `minCellVol` against time.
- A delta that widens near the end points to cause 3.
- A uniformly low pack with a small delta points to cause 4 (fade) or cause 2 (drift), with cause 2 applying when the Wh out is normal.

**3. Load step.** Compare `minCellVol` under, say, 50 W against 200 W+ at the same SoC. A large difference in sag means high internal resistance, either in one cell (cause 3) or across the pack (cause 4), depending on the delta.

**4. Post-Cutout rest.** Log the rested `minCellVol` and `maxCellVol`, and the change in `lcdShowSoc` versus `soc`, to capture the Rebound mechanism.

**5. Settings snapshot.** Record `minDsgSoc`, `maxChargeSoc`, Backup Reserve, the timeouts, X-Boost, and the firmware version.

## EcoFlow's calibration procedure

Searches of EcoFlow's River 2 Max manual, FAQ and support pages found **no River 2 Max-specific procedure**. EcoFlow's general guidance:

| Source | Guidance |
|---|---|
| [EF-NotFull] | Run a device until the unit "completely drains to 0% and shuts off", then recharge to 100% "without interruption" from a reliable AC wall outlet. This lets the system "re-learn its upper and lower limits". Repeat every 2–3 months. |
| [EF-Recal] (power-bank focused, same principle) | Drain until the unit powers off automatically, rest 1–2 h, charge to 100% without stopping, then stay plugged in another 1–2 h. Don't recalibrate too often, because deep discharges add stress. |
| [EF-DeltaFAQ] | SoC calibration means "fully discharging and recharging the battery three times". This covers the older DELTA. |
| [EF-BMS] | Power the unit off for ≥30 min to clear temporary BMS error states. Check firmware. (It also suggests discharging to 20% and then fully recharging, which conflicts with the 0% advice above. Treat it as low weight.) |
| [Manual] | The storage instruction to discharge to 0% and then recharge confirms that EcoFlow expects 0% discharges on this unit. |

Practical form for this unit, combining the sources above (the settings changes are inference):

1. Set Min Discharge Level to 0% and Max Charge Level to 100%. Disable Backup Reserve, and set Unit and AC Timeout to Never.
2. Update the firmware.
3. Discharge at a moderate steady load until the unit shuts itself off.
4. Rest 1–2 h.
5. Charge uninterrupted on AC to 100% and leave it connected a while longer.
6. Repeat up to 3×.

If the Cutout percentage and Runtime don't improve after 3 cycles, the cause is physical (causes 3 or 4), not calibration.

## Warranty: terms and evidence expectations

- **Term:** River 2 Max **5 years / 60 months** [EF-Warranty-US] [EF-Policy].
- **What EcoFlow asks for:** the **serial number** and the **original proof of purchase and/or proof of delivery**, showing the date and product details. The policy also asks you to describe the defect and follow its service procedure. The US process is mail-in only, with EcoFlow-provided prepaid labels [EF-Warranty-US] [EF-Policy].
  - If the purchase date can't be confirmed, the international policy starts the warranty at the manufacturing date (from the serial number) plus 90 days [EF-Policy].
- **Exclusions:**
  - "normal wear and tear (including, without limitation, wear and tear of batteries, if applicable)"
  - batteries that have been short-circuited, have broken or tampered seals, or were used in equipment they weren't specified for
  - unauthorized modifications or parts
  - storage without a charge or discharge for >6 months [Manual] [EF-Policy]
- **No published capacity threshold** (such as "<80% = defect") [EF-Warranty-US] [EF-Policy]. The only quantitative claim to argue against is the spec of **"80%+ capacity after 3000 cycles"** [Manual].
- **Evidence:** EcoFlow publishes no requirements beyond the above. The following package is our recommendation, not EcoFlow's:
  - Test Cycle graphs of the cell delta and the minimum cell voltage at the Cutout
  - Wh delivered vs 512 Wh
  - `cycles`, `soh`, `fullCap/designCap`
  - firmware version
  - screenshots showing the discharge limit at 0%
  - a short video of the Cutout, Rebound and Collapse to zero
  - a note that calibration cycles were done without improvement

  The strongest argument against "normal wear" is a widening cell delta, or a capacity well below spec at a low cycle count.

## Gaps and caveats

- The River 2 Max cutoff voltages, balancing method, and SoC algorithm are not published by EcoFlow.
- The field mapping is community-maintained [HA-R2Max]. Units (mV vs V) need confirming against live data.
- I found no River 2 Max-specific firmware known issue or official calibration FAQ. The original "RIVER Max" FAQ (discharge to 0%, charge until there is no input, up to 3×) was seen only in a search summary and not verified.
- The Rebound mechanism (whether the BMS re-estimates SoC from open-circuit voltage at power-on) is inferred, not documented by EcoFlow.

## Sources

- [Manual] EcoFlow RIVER 2 Max User Manual V1.0 (EN): https://websiteoss.ecoflow.com/cms/upload/2023/1/17/ECOFLOW%20RIVER%202%20Max-User%20Manual%20(EN%2BFR%2BCHT)%20V1.0_1673944511790.pdf and https://websiteoss.ecoflow.com/cms/upload/2023/3/20/EcoFlow%20RIVER%202%20Max-User%20Manual%20(EN)%20V1.0_1679286884683.pdf. The text was extracted locally and the quotes above are verbatim.
- [EF-Warranty-US] https://us.ecoflow.com/pages/warranty-policy
- [EF-Policy] https://www.ecoflow.com/us/support/policy
- [EF-NotFull] https://www.ecoflow.com/us/blog/power-station-not-charging-fully-and-fix
- [EF-Recal] https://www.ecoflow.com/us/blog/recalibrate-power-bank-battery
- [EF-BMS] https://www.ecoflow.com/us/blog/troubleshooting-your-bms
- [EF-DeltaFAQ] https://www.ecoflow.com/us/blog/delta-faq-everything-you-need-to-know
- [BU-903] Battery University, How to Measure State-of-charge: https://batteryuniversity.com/article/bu-903-how-to-measure-state-of-charge
- [BU-803a] Battery University, Cell Matching and Balancing: https://batteryuniversity.com/article/bu-803a-cell-matching-and-balancing
- [HA-R2Max] hassio-ecoflow-cloud, River 2 Max device doc (community): https://github.com/tolwi/hassio-ecoflow-cloud/blob/main/docs/devices/RIVER_2_MAX.md
- [LFP-sag] Secondary, for cutoff and sag ranges only: https://www.wevolver.com/article/lifepo4-voltage-chart-soc-voltages-for-32v12v24v48v-systems ; SDSU LFP ageing paper https://chrismi.sdsu.edu/publications/225.pdf
- [Bluetti-AC200Max] Secondary analogue, a user explanation of under-voltage cutoff with SoC still showing: https://community.bluettipower.com/t/ac200max-not-reliable-below-20-charge/9077
