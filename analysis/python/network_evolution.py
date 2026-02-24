"""Fig05 & Fig06: Network evolution under dynamic rewiring."""
import os
import numpy as np
import matplotlib.pyplot as plt
from config import (FIGURES_DIR, RESULTS_DIR, BDP_LEVELS, CELL_COLORS,
                    FACTORIAL_CELLS, read_terminal)

# --- Fig05: Mean degree comparison across factorial cells ---
fig, ax = plt.subplots(figsize=(10, 6))

for cell_name in ["static_static", "endo_static", "static_dynamic", "endo_dynamic"]:
    cell_dir = os.path.join(RESULTS_DIR, "c1_factorial", cell_name)
    bdps_valid = []
    means = []
    stds = []
    for bdp in BDP_LEVELS:
        fname = f"c1_{cell_name}_bdp{bdp}_terminal.csv"
        fpath = os.path.join(cell_dir, fname)
        if os.path.exists(fpath):
            df = read_terminal(fpath)
            if "MeanDegree" in df.columns:
                bdps_valid.append(bdp)
                means.append(df["MeanDegree"].mean())
                stds.append(df["MeanDegree"].std())

    if bdps_valid:
        ax.plot(bdps_valid, means, "o-", markersize=3, linewidth=1.5,
                color=CELL_COLORS[cell_name],
                label=FACTORIAL_CELLS[cell_name]["label"])
        ax.fill_between(bdps_valid,
                        [m - s for m, s in zip(means, stds)],
                        [m + s for m, s in zip(means, stds)],
                        alpha=0.15, color=CELL_COLORS[cell_name])

ax.set_xlabel("BDP (PLN)")
ax.set_ylabel("Mean Degree at M120")
ax.set_title("Network Mean Degree: Factorial Comparison")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig05_mean_degree_factorial.png")
plt.close()
print("Saved fig05_mean_degree_factorial.png")

# --- Fig06: Mean degree vs BDP for different rho values ---
fig, ax = plt.subplots(figsize=(10, 6))

from config import RHOS, RHO_COLORS

for i, rho in enumerate(RHOS):
    rho_safe = str(rho).replace(".", "_")
    bdps_valid = []
    means = []
    for bdp in BDP_LEVELS:
        fname = f"c3_rho{rho_safe}_bdp{bdp}_terminal.csv"
        fpath = os.path.join(RESULTS_DIR, "c3_rho", fname)
        if os.path.exists(fpath):
            df = read_terminal(fpath)
            if "MeanDegree" in df.columns:
                bdps_valid.append(bdp)
                means.append(df["MeanDegree"].mean())

    if bdps_valid:
        ax.plot(bdps_valid, means, "o-", markersize=3, linewidth=1.5,
                color=RHO_COLORS[i], label=f"$\\rho={rho}$")

ax.set_xlabel("BDP (PLN)")
ax.set_ylabel("Mean Degree at M120")
ax.set_title(r"Network Mean Degree vs BDP for different $\rho$")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig06_mean_degree_rho.png")
plt.close()
print("Saved fig06_mean_degree_rho.png")
