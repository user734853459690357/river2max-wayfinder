# EcoFlow River 2 Max diagnosis

Language for diagnosing why the user's River 2 Max power station turns off before its battery is actually empty.

## Language

**Displayed SoC**:
The battery percentage the unit shows on its screen or in the app. It is the unit's own estimate and may be wrong.
_Avoid_: charge, battery level, percent

**Cutout**:
The unit powers itself off completely, with the screen going dark, while it is powering a load and the Displayed SoC is still well above 0% (usually around 25%, or about 20% under loads over 200 W).
_Avoid_: turn off, shutdown, crash

**Rebound**:
After a Cutout, the Displayed SoC reads higher when the unit is turned back on (e.g. 33% or 47%), or it keeps running normally with no load attached.
_Avoid_: recovery

**Collapse to zero**:
After a Cutout and Rebound, plugging a load back in causes another Cutout, after which the Displayed SoC reads 0%.

**Runtime**:
How long the unit powers a given load, from 100% Displayed SoC until the Cutout. It used to be 3.5–4 h and is now about 2.5 h.
_Avoid_: battery life

**Test Cycle**:
One deliberate, monitored run: discharge under a load from 100% until the Cutout, then charge from there back to 100%.

**Usable capacity**:
The charge (Ah) the pack actually delivers between a full charge and the Cutout, as measured in a Test Cycle. It is distinct from the capacity the unit reports about itself.
_Avoid_: capacity, full capacity, health (when this meaning is intended)

**Fault report**:
The owner's factual written account of the defect, backed by Test Cycle data, that goes with the warranty claim.
_Avoid_: summary, AI report
