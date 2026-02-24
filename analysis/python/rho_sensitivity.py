"""Fig09 & Fig10: Rho sensitivity analysis."""
import numpy as np
import matplotlib.pyplot as plt
from config import (FIGURES_DIR, RHOS, RHO_COLORS, BDP_LEVELS,
                    load_rho_sweep, adoption_curve, find_critical_bdp)

# --- Fig09: Adoption curves for each rho ---
fig, ax = plt.subplots(figsize=(10, 6))

bdp_c_values = []
for i, rho in enumerate(RHOS):
    data = load_rho_sweep(rho)
    bdps, means, stds = adoption_curve(data)
    if bdps:
        ax.plot(bdps, [m * 100 for m in means], "o-", markersize=3,
                linewidth=1.5, color=RHO_COLORS[i],
                label=f"$\\rho={rho}$")
        ax.fill_between(bdps,
                        [(m - s) * 100 for m, s in zip(means, stds)],
                        [(m + s) * 100 for m, s in zip(means, stds)],
                        alpha=0.1, color=RHO_COLORS[i])
        bdp_c = find_critical_bdp(bdps, stds)
        bdp_c_values.append((rho, bdp_c))

ax.set_xlabel("BDP (PLN)")
ax.set_ylabel("Total Adoption (%)")
ax.set_title(r"Adoption vs BDP: $\rho$ sensitivity ($\lambda=0$)")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig09_rho_adoption.png")
plt.close()
print("Saved fig09_rho_adoption.png")

# --- Fig10: BDP_c vs rho ---
fig, ax = plt.subplots(figsize=(8, 5))

rhos_plot = [x[0] for x in bdp_c_values if x[1] is not None]
bdp_c_plot = [x[1] for x in bdp_c_values if x[1] is not None]

if rhos_plot:
    ax.plot(rhos_plot, bdp_c_plot, "ko-", markersize=8, linewidth=2)
    ax.set_xlabel(r"$\rho$ (rewiring rate)")
    ax.set_ylabel(r"$BDP_c$ (PLN)")
    ax.set_title(r"Critical BDP vs Rewiring Rate $\rho$")
    ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig10_bdpc_vs_rho.png")
plt.close()
print("Saved fig10_bdpc_vs_rho.png")
