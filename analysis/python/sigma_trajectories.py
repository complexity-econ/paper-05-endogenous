"""Fig03 & Fig04: Sigma trajectories + final sigma heatmap."""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import (FIGURES_DIR, RESULTS_DIR, BDP_LEVELS,
                    SECTOR_NAMES, SECTOR_SIGMA_COLS, BASE_SIGMAS,
                    read_terminal)

# For sigma trajectories, we need timeseries data.
# Since campaigns only save terminal CSVs, we use terminal sigma values
# across BDP levels to show the relationship.

# --- Fig03: Final sigma vs BDP for endo_static cell ---
fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharex=True)
axes = axes.flatten()

cell_dir = os.path.join(RESULTS_DIR, "c1_factorial", "endo_static")
for s_idx, (s_name, s_col, base_sig) in enumerate(
        zip(SECTOR_NAMES, SECTOR_SIGMA_COLS, BASE_SIGMAS)):
    ax = axes[s_idx]
    bdps_valid = []
    means = []
    stds = []
    for bdp in BDP_LEVELS:
        fname = f"c1_endo_static_bdp{bdp}_terminal.csv"
        fpath = os.path.join(cell_dir, fname)
        if os.path.exists(fpath):
            df = read_terminal(fpath)
            if s_col in df.columns:
                bdps_valid.append(bdp)
                means.append(df[s_col].mean())
                stds.append(df[s_col].std())

    if bdps_valid:
        ax.plot(bdps_valid, means, "o-", markersize=3, linewidth=1.5)
        ax.fill_between(bdps_valid,
                        [m - s for m, s in zip(means, stds)],
                        [m + s for m, s in zip(means, stds)],
                        alpha=0.2)
        ax.axhline(base_sig, color="red", linestyle="--", alpha=0.5,
                   label=f"Base={base_sig}")
        ax.axhline(base_sig * 3.0, color="gray", linestyle=":", alpha=0.3,
                   label=f"Cap={base_sig * 3:.0f}")

    ax.set_title(s_name, fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

axes[3].set_xlabel("BDP (PLN)")
axes[4].set_xlabel("BDP (PLN)")
axes[5].set_xlabel("BDP (PLN)")
axes[0].set_ylabel(r"$\sigma$ at M120")
axes[3].set_ylabel(r"$\sigma$ at M120")

fig.suptitle(r"Endogenous $\sigma$ at M120 vs BDP ($\lambda=0.02$, static network)",
             fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig03_sigma_vs_bdp.png")
plt.close()
print("Saved fig03_sigma_vs_bdp.png")

# --- Fig04: Sigma heatmap (BDP x Sector) ---
fig, ax = plt.subplots(figsize=(10, 5))

# Build matrix: rows=sectors, cols=BDP levels
matrix = np.full((6, len(BDP_LEVELS)), np.nan)
for j, bdp in enumerate(BDP_LEVELS):
    fname = f"c1_endo_static_bdp{bdp}_terminal.csv"
    fpath = os.path.join(cell_dir, fname)
    if os.path.exists(fpath):
        df = read_terminal(fpath)
        for s_idx, s_col in enumerate(SECTOR_SIGMA_COLS):
            if s_col in df.columns:
                # Normalize: sigma_final / sigma_base (fold change)
                matrix[s_idx, j] = df[s_col].mean() / BASE_SIGMAS[s_idx]

im = ax.imshow(matrix, aspect="auto", cmap="YlOrRd", vmin=1.0,
               interpolation="nearest")
ax.set_xticks(range(0, len(BDP_LEVELS), 2))
ax.set_xticklabels([BDP_LEVELS[i] for i in range(0, len(BDP_LEVELS), 2)],
                   rotation=45, fontsize=8)
ax.set_yticks(range(6))
ax.set_yticklabels(SECTOR_NAMES, fontsize=9)
ax.set_xlabel("BDP (PLN)")
ax.set_title(r"$\sigma_{final} / \sigma_{base}$ (fold change at M120)")
plt.colorbar(im, ax=ax, label="Fold change")
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig04_sigma_heatmap.png")
plt.close()
print("Saved fig04_sigma_heatmap.png")
