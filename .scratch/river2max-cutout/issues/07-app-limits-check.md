# Check the app's discharge limit and reserve settings

Type: task
Status: resolved
Blocked by:

## Question

In the EcoFlow app, what are the River 2 Max's Min Discharge Level and Backup Reserve set to, plus the firmware version, cycle count and any timeouts? A limit near 25% would explain part of the cutout cheaply. Record the values, and reset the limits to 0% before the Test Cycle. This is a human checklist: only the user has the app.

## Answer

User checked the app (2026-11-11): the discharge/charge limits have always been 0–100%. The firmware is updated to the latest (exact version not recorded). App limits are **ruled out** as the cause. The cycle count was not recorded; the exporter's `cycles` metric will capture it in the install ticket.
