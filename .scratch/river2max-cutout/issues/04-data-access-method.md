# How to log in to EcoFlow and get the data

Type: grilling
Status: resolved
Blocked by: 01

## Question

Which access method does the exporter use for this unit — EcoFlow developer API keys or account-login MQTT — given the metrics and sample rates each provides (from 01), and the user's comfort with credential handling? Where are the credentials stored?

## Answer

Decided with the user (2026-11-11), based on [research/01-exporter-capabilities.md](../research/01-exporter-capabilities.md):

- **Access method:** account-login MQTT, with `EXPORTER_TYPE=mqtt` pinned so the exporter can never fall back to REST. REST (developer keys) is rejected because the River 2 Max isn't documented there, it lacks the cell, voltage and capacity fields, it polls only every 30 s, and it needs a portal approval wait.
- **Account:** the user's main EcoFlow account. No secondary or shared account. Changing the password afterwards revokes the exporter's access if needed.
- **Credential storage:** in `ecoflow-monitor/` (project folder; moved from `~/ecoflow-monitor/` at user request, 2026-11-11):
  - `.env` (chmod 600) holds `ECOFLOW_EMAIL`, `ECOFLOW_DEVICES` (the River 2 Max serial) and `EXPORTER_TYPE=mqtt`.
  - `secrets/ecoflow_password` (chmod 600) is passed via `ECOFLOW_PASSWORD_FILE`.
  - No credentials go in compose files or `.scratch/` notes; the notes record locations only.
- **Password entry:** the user types it themselves (by running `ecoflow-monitor/set-password.sh`), so it never appears in the transcript. The agent writes everything else.
- **If the MQTT login fails** (Apple/Google sign-in with no password, rejected login, etc.): stop and bring it back to the user as a decision. Do not apply for developer keys automatically.

## Comments

- **2026-11-13:** at the user's request, the password moved from `secrets/ecoflow_password` into `ecoflow-monitor/.env` as `ECOFLOW_PASSWORD`. `set-password.sh` and `secrets/` were removed.
