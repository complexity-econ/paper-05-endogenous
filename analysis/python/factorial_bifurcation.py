"""Fig01 & Fig02: 2x2 factorial bifurcation diagrams + difference plot."""
import numpy as np
import matplotlib.pyplot as plt
from config import (FIGURES_DIR, FACTORIAL_CELLS, CELL_COLORS, BDP_LEVELS,
                    load_factorial_sweep, adoption_curve, find_critical_bdp)

# --- Fig01: 2x2 panel bifurcation diagrams ---
fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True, sharey=True)
cell_order = ["static_static", "endo_static", "static_dynamic", "endo_dynamic"]
positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

all_curves = {}
for cell_name, (row, col) in zip(cell_order, positions):
    ax = axes[row, col]
    cell = FACTORIAL_CELLS[cell_name]
    data = load_factorial_sweep(cell_name)
    bdps, means, stds = adoption_curve(data)
    all_curves[cell_name] = (bdps, means, stds)

    color = CELL_COLORS[cell_name]
    ax.plot(bdps, [m * 100 for m in means], color=color, linewidth=2)
    ax.fill_between(bdps,
                    [(m - s) * 100 for m, s in zip(means, stds)],
                    [(m + s) * 100 for m, s in zip(means, stds)],
                    alpha=0.2, color=color)

    bdp_c = find_critical_bdp(bdps, stds)
    if bdp_c is not None:
        ax.axvline(bdp_c, color=color, linestyle="--", alpha=0.5)
        ax.set_title(f"{cell['label']}\n$BDP_c={bdp_c}$", fontsize=10)
    else:
        ax.set_title(cell["label"], fontsize=10)

    ax.set_xlim(0, 5000)
    ax.set_ylim(0, 80)
    ax.grid(True, alpha=0.3)

axes[1, 0].set_xlabel("BDP (PLN)")
axes[1, 1].set_xlabel("BDP (PLN)")
axes[0, 0].set_ylabel("Total Adoption (%)")
axes[1, 0].set_ylabel("Total Adoption (%)")

fig.suptitle("2x2 Factorial: Adoption vs BDP", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig01_factorial_bifurcation.png")
plt.close()
print("Saved fig01_factorial_bifurcation.png")

# --- Fig02: Difference plot (each cell minus baseline) ---
fig, ax = plt.subplots(figsize=(10, 6))
baseline_bdps, baseline_means, _ = all_curves.get("static_static", ([], [], []))

for cell_name in ["endo_static", "static_dynamic", "endo_dynamic"]:
    if cell_name not in all_curves:
        continue
    bdps, means, stds = all_curves[cell_name]
    # Align BDP levels
    diff = []
    common_bdps = []
    for i, b in enumerate(bdps):
        if b in baseline_bdps:
            j = baseline_bdps.index(b)
            diff.append((means[i] - baseline_means[j]) * 100)
            common_bdps.append(b)

    ax.plot(common_bdps, diff, color=CELL_COLORS[cell_name], linewidth=2,
            label=FACTORIAL_CELLS[cell_name]["label"])

ax.axhline(0, color="black", linewidth=0.5)
ax.set_xlabel("BDP (PLN)")
ax.set_ylabel(r"$\Delta$ Adoption (pp) vs baseline")
ax.set_title("Adoption Difference from Static/Static Baseline")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig02_factorial_difference.png")
plt.close()
print("Saved fig02_factorial_difference.png")
