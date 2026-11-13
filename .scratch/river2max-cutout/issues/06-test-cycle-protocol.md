# How to run the Test Cycle

Type: grilling
Status: resolved
Blocked by: 01, 02

## Question

What is the Test Cycle protocol: which steady load (user leaning ~100–150 W, device TBD), app settings to check/reset first, what to note manually during the run (time of Cutout, Displayed SoC, Rebound value), whether to include a Collapse-to-zero step, and how the charge back to 100% is recorded?

## Comments

- From [Install and verify the monitoring setup](05-install-stack.md): the effective sample rate is about 5–10 s (polled snapshots). Current and pack voltage are whole A/V, so use `8 × min_cell_vol` for sag. The final seconds before a Cutout may be lost. Baseline: 275 cycles, full cap 86.4% of design.

## Answer

Decided with the user (2026-11-11):

1. **Start from 100%.** First charge on AC to 100% Displayed SoC (the monitor records it), then unplug the charger and note the time. That is t0.
2. **Load:** the laptop as it is normally used, on USB-C, about 40–90 W and varying. This replaces the earlier steady 100–150 W idea. The laptop also runs the monitoring: after the Cutout it falls back to its own battery, and the user plugs it into the wall soon after. Laptop sleep is covered by heavy use plus `tools/keep-awake.ps1` (see [Is this laptop ready to record a Test Cycle](03-laptop-readiness.md)).
3. **Manual notes, one line in chat each with time and screen %:** t0, the Cutout, the Rebound (unit switched on with nothing attached), then about 10 min idle.
4. **Collapse to zero:** the user will *try* it. After the idle period, re-attach the laptop until the second Cutout and 0%. It's optional if impractical.
5. **Recharge:** on AC, uninterrupted, nothing attached, to 100% (limit stays at 100%), started within about 1 h. The monitor stays up throughout to record energy in.

The data side is set by [Install and verify the monitoring setup](05-install-stack.md). Key signals are listed in [Known causes of early cutout](02-cutout-causes.md).
