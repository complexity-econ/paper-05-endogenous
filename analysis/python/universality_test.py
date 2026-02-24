"""Fig11 & Fig12: Universality comparison + SOC diagnostic."""
import os
import numpy as np
import matplotlib.pyplot as plt
from config import (FIGURES_DIR, RESULTS_DIR, FACTORIAL_CELLS, CELL_COLORS,
                    BDP_LEVELS, SECTOR_SIGMA_COLS, SECTOR_NAMES, BASE_SIGMAS,
                    load_factorial_sweep, adoption_curve, find_critical_bdp,
                    read_terminal)

# --- Fig11: Variance peaks (susceptibility proxy) across all 4 cells ---
fig, ax = plt.subplots(figsize=(10, 6))

for cell_name in ["static_static", "endo_static", "static_dynamic", "endo_dynamic"]:
    data = load_factorial_sweep(cell_name)
    bdps, means, stds = adoption_curve(data)
    if bdps:
        # Susceptibility proxy: variance = std^2
        variances = [s ** 2 * 1e4 for s in stds]  # scale for visibility
        ax.plot(bdps, variances, "o-", markersize=4, linewidth=1.5,
                color=CELL_COLORS[cell_name],
                label=FACTORIAL_CELLS[cell_name]["label"])

        bdp_c = find_critical_bdp(bdps, stds)
        if bdp_c is not None:
            ax.axvline(bdp_c, color=CELL_COLORS[cell_name],
                       linestyle="--", alpha=0.4)

ax.set_xlabel("BDP (PLN)")
ax.set_ylabel(r"Var(adoption) $\times 10^4$")
ax.set_title("Susceptibility Proxy: Variance Peaks Across Factorial Cells")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig11_universality_variance.png")
plt.close()
print("Saved fig11_universality_variance.png")

# --- Fig12: SOC diagnostic ---
# Does endogenous sigma converge to a value near the phase boundary?
# Compare final sigma values at BDP_c vs other BDP levels

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left panel: sigma trajectory across BDP for endo cells
ax = axes[0]
for cell_name in ["endo_static", "endo_dynamic"]:
    cell_dir = os.path.join(RESULTS_DIR, "c1_factorial", cell_name)
    # Average sigma across all sectors (weighted by base)
    bdps_valid = []
    avg_sigmas = []
    for bdp in BDP_LEVELS:
        fname = f"c1_{cell_name}_bdp{bdp}_terminal.csv"
        fpath = os.path.join(cell_dir, fname)
        if os.path.exists(fpath):
            df = read_terminal(fpath)
            total = 0
            count = 0
            for s_idx, s_col in enumerate(SECTOR_SIGMA_COLS):
                if s_col in df.columns:
                    # Fold change
                    total += df[s_col].mean() / BASE_SIGMAS[s_idx]
                    count += 1
            if count > 0:
                bdps_valid.append(bdp)
                avg_sigmas.append(total / count)

    if bdps_valid:
        ax.plot(bdps_valid, avg_sigmas, "o-", markersize=3, linewidth=1.5,
                color=CELL_COLORS[cell_name],
                label=FACTORIAL_CELLS[cell_name]["label"])

ax.axhline(1.0, color="black", linestyle=":", alpha=0.3, label="No change")
ax.set_xlabel("BDP (PLN)")
ax.set_ylabel(r"Mean $\sigma_{final}/\sigma_{base}$")
ax.set_title("Sigma Fold Change vs BDP (endo cells)")
ax.legend()
ax.grid(True, alpha=0.3)

# Right panel: Adoption vs sigma fold change (scatter)
ax = axes[1]
for cell_name in ["endo_static", "endo_dynamic"]:
    cell_dir = os.path.join(RESULTS_DIR, "c1_factorial", cell_name)
    fold_changes = []
    adoptions = []
    for bdp in BDP_LEVELS:
        fname = f"c1_{cell_name}_bdp{bdp}_terminal.csv"
        fpath = os.path.join(cell_dir, fname)
        if os.path.exists(fpath):
            df = read_terminal(fpath)
            total = 0
            count = 0
            for s_idx, s_col in enumerate(SECTOR_SIGMA_COLS):
                if s_col in df.columns:
                    total += df[s_col].mean() / BASE_SIGMAS[s_idx]
                    count += 1
            if count > 0:
                fold_changes.append(total / count)
                adoptions.append(df["TotalAdoption"].mean() * 100)

    if fold_changes:
        ax.scatter(fold_changes, adoptions, s=30, alpha=0.7,
                   color=CELL_COLORS[cell_name],
                   label=FACTORIAL_CELLS[cell_name]["label"])

ax.set_xlabel(r"Mean $\sigma_{final}/\sigma_{base}$")
ax.set_ylabel("Total Adoption (%)")
ax.set_title("SOC Diagnostic: Adoption vs Sigma Growth")
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig12_soc_diagnostic.png")
plt.close()
print("Saved fig12_soc_diagnostic.png")
