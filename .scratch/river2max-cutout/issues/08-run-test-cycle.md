# Run the Test Cycle

Type: task
Status: resolved
Blocked by: 06

## Question

Carry out the Test Cycle per [How to run the Test Cycle](06-test-cycle-protocol.md) with the monitor running: charge to 100%, discharge with the laptop load to the Cutout, Rebound, (try) Collapse to zero, recharge to 100%. HITL: the user handles the unit and posts timestamped notes; the agent checks telemetry stays live (msgs/min > 0, no gaps) and records the event timestamps plus the Prometheus time range of the run. Resolved when the recharge reaches 100% and the time ranges are recorded.

## Comments
- **Pre-charge:** 91% → 100% on AC between about 21:32 and 21:39 UTC (peak input 623 W).
- **t0 = 2026-11-11 21:39 UTC (23:39 local, UTC+2):** user reports 100% and the charger unplugged. Telemetry: LCD SoC 100, BMS f32 SoC 99.99, cells 3311/3311 mV (spread 0), remain_cap 17277 / full_cap 17280 mAh, input 0 W, **output 0 W at that moment**, about 35 msgs/min, online.
- **Router outage about 21:43–21:44 UTC:** the exporter lost the broker at 21:43:42, auto-reconnected, and data resumed (last message 4.6 s old at 21:44:20). Gap is about 1 min. At 21:44: 98%, 126 W out, cells 3241/3241 mV.
- **Load:** rose from about 126 W to about 230–300 W (AC output) from about 21:49 UTC onward.
- **Cutout ≈ 22:46:45–22:47:15 UTC (00:46 local):** user reports "25%".
  - **Last loaded sample (22:46:45):** LCD SoC 23.13, min cell 3001 mV, −12 A, 235 W.
  - **SoC fell fast just before the Cutout:** 30.95 → 23.13% between 22:45:45 and 22:46:45 (normal rate at this load is about 1%/min).
  - **Next sample (22:47:30):** SoC **25.49** (Rebound), 0 W, `mppt_cfg_ac_enabled` 1→0, cell relaxing 3076 → 3092 mV.
  - **The unit stayed online:** messages resumed within about 45 s. **Need from the user:** did the screen go dark (full power-off) or did only the AC output stop?
- **Energy out t0→Cutout:** ≈ **275 Wh** (integrated `pd_watts_out_sum`, 21:37–22:47). Runtime ≈ **67 min** at about 250 W average.
- **Cell spread:** max − min stayed **0 mV for the entire run**, even under 12 A. On this model min/max probably both report the same value (likely a pack average), so cell spread is **not a usable imbalance signal**.
- **User confirms:** the high load was gaming (intentional fast drain). The Cutout was a **full power-off with the screen dark**. The user switched it back on and it showed **25%** (Rebound). The ~45 s telemetry gap is the off period.
- **Re-load ≈ 23:02:15 UTC:** about 62 W on DC/USB-C (`mppt_cfg_ac_enabled` stayed 0). Cell 3108 → 3058 mV at only about −2 A within 45 s.
- **Second Cutout ≈ 23:03:00–23:03:20 UTC (01:03 local):** the user saw **24%** before and **25%** after switching back on. Last loaded sample (23:03:00): SoC 24.14, min cell **3058 mV at −2 A (~0.1C)**. After: 25.49%, 3074 mV.
  - **No Collapse to zero** on this attempt.
  - The telemetry gap was too short to see (under about 20 s).
  - Notable: the Cutout came at about 3.06 V per cell (pack average) under a very light load, far above a typical LFP cell cutoff (about 2.5 V). Combined with min = max always, this suggests the reported cell value is an average that could hide one low cell. To be weighed in [What the Test Cycle data says about the cause](09-diagnose-from-data.md).
- **Rest and repeated re-loads, 23:03–00:08 UTC.** Idle, the unit sat at 25.49% while the cell (average) recovered to about 3086–3091 mV. Every re-load cut out within about 5–20 s, at the cell readings shown, while displaying ~25%. After each one it came back at **25.49% with remain_cap reset to 4404 mAh**: the same stored value every boot.

  | Re-load | Load | Cell reading |
  |---|---|---|
  | 23:15:00 | 62 W | ~3083 mV |
  | 23:35:30 | 62 W | ~3074 mV |
  | 23:37:50 | AC output on | ~3073 mV |
  | 23:49:50 | 50 W | ~3082 mV |
  | 00:05:50 | ~4 W | — |

  There was a telemetry gap of more than 5 min at about 23:39–23:46 (unit off, so the exporter dropped the series), and another at 00:06–00:08.
- **Collapse to zero ≈ 00:07 UTC (02:07 local):** user reports **0%**. The first sample after it (00:08:40) shows LCD SoC 0, BMS SoC 0, **remain_cap 0**, and the resting cell (average) at **3079 mV**, i.e. the BMS declared empty at a resting voltage that is still well above an empty LFP cell.
- **Next:** uninterrupted AC recharge to 100% with nothing attached.
- **Recharge start ≈ 00:11 UTC (02:11 local):** AC input ramped to about 590 W. SoC 0 → 2% within a minute, cell (average) 3078 → 3298 mV under charge.
- **Recharge done:** LCD SoC first read **100% at 00:46:30 UTC** (user: "100% 2:47" local), about 35 min after the start.
  - **Energy in (AC input):** ≈ **348 Wh** (integrated `pd_watts_in_sum`, 00:10–00:50), peak 620 W.
  - **The SoC jumped near the top:** 44% (00:35) → 63% (00:40) → 99% (00:45). Gaining 55% in 10 min at about 600 W is physically impossible, so the SoC was re-anchored at the top of charge.
  - **After:** remain_cap = full_cap = **17460** mAh (full_cap was 17280 before), cycles 275, soh 97, cell 3339 mV.
  - There was one telemetry gap of up to about 3 min during the charge.

## Answer

**Test Cycle completed and recorded, 2026-11-11 → 12.** All times UTC; local is UTC+2.

- **Prometheus range:** 2026-11-11 21:30 → 2026-11-12 00:50 UTC. Query on localhost:9090 or view in Grafana under "River 2 Max — Test Cycle". The step-by-step log with timestamps and readings is in the Comments above.

| Event | UTC | Displayed SoC | Cell (avg) | Load / notes |
|---|---|---|---|---|
| t0, charger off | 21:39 | 100% | 3311 mV | — |
| Cutout 1 | ≈22:46:50 | 23% → Rebound 25% | 3001 mV at −12 A | 230–300 W (gaming); SoC fell 31→23% in the last minute |
| Cutout 2 | ≈23:03:10 | 24% → 25% | 3058 mV at −2 A | ~62 W DC |
| Re-loads ×5 | 23:15–00:06 | 25.49% each boot | ~3073–3083 mV | 4–62 W; each cut out within 5–20 s |
| Collapse to zero | ≈00:07 | 0% (remain_cap 0) | 3079 mV at rest | — |
| Recharge | 00:11 → 00:46:30 | 0 → 100% | → 3339 mV | ~590–620 W AC, nothing attached |

- **Energy:** ≈ **275 Wh out** from 100% to Cutout 1 (rated 512 Wh) and ≈ **348 Wh in** at the AC socket from 0 to 100%.
- **Runtime:** 67 min at about 250 W average.
- **Data limits:**
  - Min and max cell are always equal, so there is no per-cell visibility.
  - Current and voltage are reported in whole A and V.
  - Telemetry gaps: about 1 min (router, 21:43), more than 5 min (unit off, 23:39–23:46), about 2 min (00:06–00:08), and up to about 3 min during the recharge.
