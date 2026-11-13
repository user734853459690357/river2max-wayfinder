# PROTOTYPE: renders the Fault report figures from the recorded Prometheus data.
import json, urllib.request, urllib.parse, datetime as dt, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md

PROM = sys.argv[1]; OUT = sys.argv[2]; LANG = sys.argv[3] if len(sys.argv) > 3 else "en"
SUF = "" if LANG == "en" else f"-{LANG}"
TR = {"uk": {
    "Displayed SoC (%)": "Заряд на дисплеї (%)", "Avg cell voltage (V)": "Середня напруга комірки (В)",
    "Output (W)": "Вихідна потужність (Вт)", "AC input (W)": "Вхід від мережі (Вт)",
    "Battery current (A)": "Струм батареї (А)", "Charge current (A)": "Струм заряду (А)",
    "Cell temp (°C)": "Температура комірок (°C)",
    "Local time (UTC+2), 11–12 Nov 2026": "Місцевий час (UTC+2), 11–12 листопада 2026",
    "Figure 1 — Full test session: discharge, repeated shutdowns, recharge":
        "Рисунок 1 — Повний тест: розряд, повторні вимкнення, заряд",
    "Shutdown 1": "Вимкнення 1", "Shutdown 2": "Вимкнення 2", "Displays 0 %": "Показує 0 %",
    "AC charge": "Заряд від мережі",
    "Figure 2 — Discharge from 100 % to shutdown (avg ≈ 250 W load)":
        "Рисунок 2 — Розряд від 100 % до вимкнення (середнє навантаження ≈ 250 Вт)",
    "Unit powered off at 23 %": "Вимкнення при 23 %",
    "Figure 3 — Shutdown close-up: SoC drops 36 → 23 % in 4 min, unit powers off, restarts at 25.5 %":
        "Рисунок 3 — Момент вимкнення: заряд падає 36 → 23 % за 4 хв, вимкнення, після ввімкнення 25,5 %",
    "Power off at 23 %": "Вимкнення при 23 %", "Restart: 25.5 %": "Увімкнення: 25,5 %",
    "Figure 4 — AC recharge from 0 %: SoC jumps 44 → 99 % in 9 min at constant 19 A":
        "Рисунок 4 — Заряд від мережі з 0 %: стрибок 44 → 99 % за 9 хв при сталому струмі 19 А",
    "Rated capacity": "Номінальна ємність", "Specified: 80 % after 3000 cycles": "Специфікація: 80 % після 3000 циклів",
    "Full capacity reported by BMS": "Повна ємність за даними BMS",
    "Measured: discharge 100 % → shutdown": "Виміряно: розряд 100 % → вимкнення",
    "Measured: recharge 0 % → 100 %": "Виміряно: заряд 0 % → 100 %",
    "Ah": "А·год",
    "Figure 5 — Usable capacity vs rated and reported capacity (at 275 cycles)":
        "Рисунок 5 — Корисна, номінальна та заявлена BMS ємність (275 циклів)",
}}.get(LANG, {})
def tr(x): return TR.get(x, x)
def num(v, d=1):
    t = f"{v:.{d}f}"
    return t.replace(".", ",") if LANG == "uk" else t
LOCAL = dt.timezone(dt.timedelta(hours=2))
M = dict(soc="ecoflow_bms_ems_status_f32_lcd_show_soc", cell="ecoflow_bms_bms_status_min_cell_vol",
         amp="ecoflow_bms_bms_status_amp", out="ecoflow_pd_watts_out_sum", inw="ecoflow_pd_watts_in_sum",
         temp="ecoflow_bms_bms_status_max_cell_temp")

def get(key, start, end, step="5s"):
    q = urllib.parse.urlencode(dict(query=f"max({M[key]})", start=start, end=end, step=step))
    r = json.load(urllib.request.urlopen(f"{PROM}/api/v1/query_range?{q}"))["data"]["result"]
    pts = [(dt.datetime.fromtimestamp(float(t), LOCAL), float(v)) for t, v in (r[0]["values"] if r else [])]
    # break lines across telemetry gaps (> 60 s)
    xs, ys = [], []
    for i, (t, v) in enumerate(pts):
        if i and (t - pts[i-1][0]).total_seconds() > 60:
            xs.append(t); ys.append(float("nan"))
        xs.append(t); ys.append(v)
    return xs, ys

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": .3, "figure.dpi": 150})
fmt = md.DateFormatter("%H:%M", tz=LOCAL)
def T(s): return dt.datetime.fromisoformat(s).replace(tzinfo=LOCAL)

def panels(start, end, rows, title, fname, notes=(), step="5s"):
    s = T(start).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    e = T(end).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fig, axs = plt.subplots(len(rows), 1, figsize=(10, 2.3*len(rows)+.6), sharex=True)
    for ax, (key, label, color, scale) in zip(axs, rows):
        x, y = get(key, s, e, step)
        ax.plot(x, [v*scale for v in y], color=color, lw=1.4)
        ax.set_ylabel(tr(label))
    for n, (ax_i, when, text) in enumerate(notes):
        axs[ax_i].axvline(T(when), color="#b00", ls="--", lw=.9)
        axs[ax_i].annotate(tr(text), (T(when), axs[ax_i].get_ylim()[1]), xytext=(4, -10 - 14*(n % 2)), textcoords="offset points",
                           fontsize=8.5, color="#b00", va="top")
    axs[-1].xaxis.set_major_formatter(fmt); axs[-1].set_xlabel(tr("Local time (UTC+2), 11–12 Nov 2026"))
    fig.suptitle(tr(title), fontsize=12, fontweight="bold"); fig.tight_layout()
    fig.savefig(f"{OUT}/{fname.replace('.png', SUF + '.png')}"); plt.close(fig)

# Figure 1 — whole session overview
panels("2026-11-11T23:30:00", "2026-11-12T02:52:00",
       [("soc", "Displayed SoC (%)", "#1f5fa8", 1), ("cell", "Avg cell voltage (V)", "#2a8a3a", .001),
        ("out", "Output (W)", "#c06000", 1), ("inw", "AC input (W)", "#6a3d9a", 1)],
       "Figure 1 — Full test session: discharge, repeated shutdowns, recharge", "fig1-session-overview.png",
       notes=[(0, "2026-11-12T00:46:50", "Shutdown 1"), (0, "2026-11-12T01:03:10", "Shutdown 2"),
              (0, "2026-11-12T02:07:00", "Displays 0 %"), (0, "2026-11-12T02:11:00", "AC charge")], step="10s")

# Figure 2 — discharge 100 % to shutdown
panels("2026-11-11T23:38:00", "2026-11-12T00:50:00",
       [("soc", "Displayed SoC (%)", "#1f5fa8", 1), ("cell", "Avg cell voltage (V)", "#2a8a3a", .001),
        ("amp", "Battery current (A)", "#c06000", 1)],
       "Figure 2 — Discharge from 100 % to shutdown (avg ≈ 250 W load)", "fig2-discharge.png",
       notes=[(0, "2026-11-12T00:46:50", "Unit powered off at 23 %")])

# Figure 3 — shutdown close-up
panels("2026-11-12T00:40:00", "2026-11-12T00:52:00",
       [("soc", "Displayed SoC (%)", "#1f5fa8", 1), ("cell", "Avg cell voltage (V)", "#2a8a3a", .001),
        ("out", "Output (W)", "#c06000", 1)],
       "Figure 3 — Shutdown close-up: SoC drops 36 → 23 % in 4 min, unit powers off, restarts at 25.5 %",
       "fig3-shutdown-closeup.png",
       notes=[(0, "2026-11-12T00:46:50", "Power off at 23 %"), (0, "2026-11-12T00:47:30", "Restart: 25.5 %")])

# Figure 4 — recharge
panels("2026-11-12T02:08:00", "2026-11-12T02:52:00",
       [("soc", "Displayed SoC (%)", "#1f5fa8", 1), ("amp", "Charge current (A)", "#c06000", 1),
        ("cell", "Avg cell voltage (V)", "#2a8a3a", .001), ("temp", "Cell temp (°C)", "#a02020", 1)],
       "Figure 4 — AC recharge from 0 %: SoC jumps 44 → 99 % in 9 min at constant 19 A",
       "fig4-recharge.png",
       notes=[(0, "2026-11-12T02:35:00", "44 %"), (0, "2026-11-12T02:44:00", "99 %")])

# Figure 5 — capacity comparison
fig, ax = plt.subplots(figsize=(10, 3.6))
labels = ["Rated capacity", "Specified: 80 % after 3000 cycles", "Full capacity reported by BMS",
          "Measured: discharge 100 % → shutdown", "Measured: recharge 0 % → 100 %"]
vals = [20.0, 16.0, 17.46, 11.2, 11.0]
cols = ["#7f7f7f", "#b0b0b0", "#1f5fa8", "#c06000", "#c06000"]
labels = [tr(l) for l in labels]
b = ax.barh(labels[::-1], vals[::-1], color=cols[::-1])
for rect, v in zip(b, vals[::-1]):
    ax.text(v + .2, rect.get_y()+rect.get_height()/2, f"{num(v)} {tr('Ah')} ({v/20*100:.0f} %)", va="center", fontsize=9)
ax.set_xlim(0, 24); ax.set_xlabel(tr("Ah")); ax.grid(axis="y", visible=False)
ax.set_title(tr("Figure 5 — Usable capacity vs rated and reported capacity (at 275 cycles)"), fontweight="bold")
fig.tight_layout(); fig.savefig(f"{OUT}/fig5-capacity{SUF}.png"); plt.close(fig)
print("ok")
