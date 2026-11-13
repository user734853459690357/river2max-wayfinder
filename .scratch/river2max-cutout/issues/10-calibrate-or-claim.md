# Calibrate first or claim the warranty now

Type: grilling
Status: resolved
Blocked by: 09

## Question

Given [What the Test Cycle data says about the cause](09-diagnose-from-data.md), should we run 1–3 more calibration cycles before claiming the warranty, or claim now?

Context:
- The Test Cycle was already one EcoFlow-style calibration cycle (a full drain until the unit shuts itself off, then an uninterrupted AC charge), and full_cap did not drop.
- Calibration would mainly test whether EcoFlow will expect it to have been tried.

Settle the claim's preconditions:
- the purchase date and whether proof is available (the warranty is 5 years; without proof it runs from the manufacturing date + 90 days)
- the region and claim channel (mail-in)
- whether "normal wear and tear" is a realistic objection at 275 cycles

## Answer

**Agreed with the user on 2026-11-12: claim the warranty now. No more calibration.**

- **Calibration is already exhausted.** The user has done **5+ full drain-to-0 / charge-to-100% cycles** with no improvement. The recorded Test Cycle is one more on top of those, and full_cap did not drop after it. Further cycles would only stress the suspected weak cell.
- **Claim channel: the authorized dealer the unit was bought from.**
  - The user has proof of purchase.
  - The user has already contacted the dealer and received the shipping details.
  - The River 2 Max launched in 2023, so the unit is inside the 5-year warranty even under the fallback rule (manufacturing date + 90 days).
- **"Normal wear and tear" is a weak objection, and the Fault report pre-empts it.**
  - The unit holds 55% Usable capacity after 275 cycles, against the spec of "80%+ capacity after 3000 cycles".
  - The BMS itself reports soh 97.
  - The user did not answer this question directly in two rounds; it was confirmed in the final summary.
- **Form of the evidence:** a **Fault report** (see `GLOSSARY.md`). It is a factual owner's technical report: measurements, method, charts and numbers, in the owner's voice.
  - **No mention of AI, assistants or tooling**, and no speculative tone beyond "suspected low-capacity cell".
  - It is delivered **printed in the box** and **emailed to the dealer before shipping**.
- **Next step:** the agent builds the **full** package (report, the four agreed charts, key numbers, app screenshots, and a video if worthwhile). **The user reviews it before anything is sent.**
