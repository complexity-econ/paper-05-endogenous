"""Fig07 & Fig08: Lambda sensitivity analysis."""
import numpy as np
import matplotlib.pyplot as plt
from config import (FIGURES_DIR, LAMBDAS, LAMBDA_COLORS, BDP_LEVELS,
                    load_lambda_sweep, adoption_curve, find_critical_bdp)

# --- Fig07: Adoption curves for each lambda ---
fig, ax = plt.subplots(figsize=(10, 6))

bdp_c_values = []
for i, lam in enumerate(LAMBDAS):
    data = load_lambda_sweep(lam)
    bdps, means, stds = adoption_curve(data)
    if bdps:
        ax.plot(bdps, [m * 100 for m in means], "o-", markersize=3,
                linewidth=1.5, color=LAMBDA_COLORS[i],
                label=f"$\\lambda={lam}$")
        ax.fill_between(bdps,
                        [(m - s) * 100 for m, s in zip(means, stds)],
                        [(m + s) * 100 for m, s in zip(means, stds)],
                        alpha=0.1, color=LAMBDA_COLORS[i])
        bdp_c = find_critical_bdp(bdps, stds)
        bdp_c_values.append((lam, bdp_c))

ax.set_xlabel("BDP (PLN)")
ax.set_ylabel("Total Adoption (%)")
ax.set_title(r"Adoption vs BDP: $\lambda$ sensitivity ($\rho=0$)")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig07_lambda_adoption.png")
plt.close()
print("Saved fig07_lambda_adoption.png")

# --- Fig08: BDP_c vs lambda ---
fig, ax = plt.subplots(figsize=(8, 5))

lams_plot = [x[0] for x in bdp_c_values if x[1] is not None]
bdp_c_plot = [x[1] for x in bdp_c_values if x[1] is not None]

if lams_plot:
    ax.plot(lams_plot, bdp_c_plot, "ko-", markersize=8, linewidth=2)
    ax.set_xlabel(r"$\lambda$ (learning rate)")
    ax.set_ylabel(r"$BDP_c$ (PLN)")
    ax.set_title(r"Critical BDP vs Learning Rate $\lambda$")
    ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(f"{FIGURES_DIR}/fig08_bdpc_vs_lambda.png")
plt.close()
print("Saved fig08_bdpc_vs_lambda.png")
