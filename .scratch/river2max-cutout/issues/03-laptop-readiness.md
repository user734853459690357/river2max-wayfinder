# Is this laptop ready to record a Test Cycle

Type: task
Status: resolved
Blocked by:

## Question

Can this WSL laptop run the exporter stack for a multi-hour Test Cycle? Check: Docker / docker compose available in WSL (or Docker Desktop integration), network reachability to EcoFlow cloud, and how to keep Windows + WSL from sleeping during the run. Record what was found and anything installed or configured.

## Answer

**Yes, the laptop is ready.** The one thing to handle is sleep, and the fix is ready (below). Checked 2026-11-11:

- **Docker:** Docker Desktop with WSL integration (engine 29.9.3, Compose v5.7.0). `docker run hello-world` works from WSL. Docker Desktop must be running on Windows during the Test Cycle. Nothing was installed.
- **Resources:** 32 cores, 15 GiB RAM (13 GiB free), 941 GB disk free. That is plenty. `git` is present, `go` is not, so we use the exporter's prebuilt image, not a local build.
- **Network to EcoFlow:** `api.ecoflow.com` / `api-e.ecoflow.com` HTTPS answers in about 0.15 s. `mqtt.ecoflow.com` and `mqtt-e.ecoflow.com` resolve (EU endpoints), and TCP 8883 (MQTT/TLS) is open to `mqtt-e`. Both access methods are reachable.
- **Sleep risk:** the Balanced plan idles to sleep after **5 min on AC** (and 3 min on battery). The machine uses Modern Standby, which **disconnects the network**, so the run would stop logging. Hibernate is off on AC. The laptop was on AC at 100% charge. Lid-close action is not exposed by `powercfg`, so **keep the lid open**.
- **Fix, with no settings changed:** `.scratch/river2max-cutout/tools/keep-awake.ps1` holds `SetThreadExecutionState(ES_CONTINUOUS|ES_SYSTEM_REQUIRED)` for N hours. Run it from a Windows terminal (not through WSL, where a parent `timeout` would kill it): `powershell -ExecutionPolicy Bypass -File keep-awake.ps1 -Hours 8`. Closing it restores normal sleep. *Unverified:* `powercfg /requests` needs admin, so we couldn't confirm the request was registered. Fallback: `powercfg /change standby-timeout-ac 0` before the run, then `powercfg /change standby-timeout-ac 5` after.
- **Implication for the setup ticket:** run the prebuilt exporter image with Docker Desktop. Keep the laptop on AC with the lid open and keep-awake running.
