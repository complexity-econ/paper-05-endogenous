"""Shared configuration for Paper-05 analysis scripts."""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS_DIR = os.path.join(BASE_DIR, "simulations", "results")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# --- Matplotlib defaults ---
plt.rcParams.update({
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
})

# --- Sweep grids ---
BDP_LEVELS = list(range(0, 5001, 250))  # 21 levels: 0, 250, ..., 5000
LAMBDAS = [0, 0.005, 0.01, 0.02, 0.05, 0.1]
RHOS = [0, 0.02, 0.05, 0.1, 0.2, 0.5]

# --- Factorial cells ---
FACTORIAL_CELLS = {
    "static_static":   {"lambda": 0,    "rho": 0,   "label": r"Static $\sigma$ / Static Net"},
    "endo_static":     {"lambda": 0.02, "rho": 0,   "label": r"Endo $\sigma$ / Static Net"},
    "static_dynamic":  {"lambda": 0,    "rho": 0.1, "label": r"Static $\sigma$ / Dynamic Net"},
    "endo_dynamic":    {"lambda": 0.02, "rho": 0.1, "label": r"Endo $\sigma$ / Dynamic Net"},
}

# --- Colors ---
CELL_COLORS = {
    "static_static":  "#1f77b4",  # blue
    "endo_static":    "#ff7f0e",  # orange
    "static_dynamic": "#2ca02c",  # green
    "endo_dynamic":   "#d62728",  # red
}

LAMBDA_COLORS = plt.cm.viridis([i / (len(LAMBDAS) - 1) for i in range(len(LAMBDAS))])
RHO_COLORS = plt.cm.plasma([i / (len(RHOS) - 1) for i in range(len(RHOS))])

SECTOR_NAMES = ["BPO/SSC", "Manufacturing", "Retail/Services",
                "Healthcare", "Public", "Agriculture"]
SECTOR_SIGMA_COLS = ["BPO_Sigma", "Manuf_Sigma", "Retail_Sigma",
                     "Health_Sigma", "Public_Sigma", "Agri_Sigma"]
BASE_SIGMAS = [50.0, 10.0, 5.0, 2.0, 1.0, 3.0]

# --- CSV helper ---
def read_terminal(path):
    """Read a terminal CSV (European format: semicolon sep, comma decimals)."""
    return pd.read_csv(path, sep=";", decimal=",")


def load_factorial_sweep(cell_name):
    """Load all BDP levels for a factorial cell. Returns dict: bdp -> DataFrame."""
    cell_dir = os.path.join(RESULTS_DIR, "c1_factorial", cell_name)
    data = {}
    for bdp in BDP_LEVELS:
        fname = f"c1_{cell_name}_bdp{bdp}_terminal.csv"
        fpath = os.path.join(cell_dir, fname)
        if os.path.exists(fpath):
            data[bdp] = read_terminal(fpath)
    return data


def load_lambda_sweep(lam):
    """Load all BDP levels for a given lambda. Returns dict: bdp -> DataFrame."""
    lam_safe = str(lam).replace(".", "_")
    data = {}
    for bdp in BDP_LEVELS:
        fname = f"c2_lam{lam_safe}_bdp{bdp}_terminal.csv"
        fpath = os.path.join(RESULTS_DIR, "c2_lambda", fname)
        if os.path.exists(fpath):
            data[bdp] = read_terminal(fpath)
    return data


def load_rho_sweep(rho):
    """Load all BDP levels for a given rho. Returns dict: bdp -> DataFrame."""
    rho_safe = str(rho).replace(".", "_")
    data = {}
    for bdp in BDP_LEVELS:
        fname = f"c3_rho{rho_safe}_bdp{bdp}_terminal.csv"
        fpath = os.path.join(RESULTS_DIR, "c3_rho", fname)
        if os.path.exists(fpath):
            data[bdp] = read_terminal(fpath)
    return data


def adoption_curve(sweep_data):
    """From a bdp->DataFrame sweep, compute mean and std of TotalAdoption at each BDP."""
    bdps, means, stds = [], [], []
    for bdp in sorted(sweep_data.keys()):
        df = sweep_data[bdp]
        bdps.append(bdp)
        means.append(df["TotalAdoption"].mean())
        stds.append(df["TotalAdoption"].std())
    return bdps, means, stds


def find_critical_bdp(bdps, stds):
    """Find BDP_c = argmax(std(adoption)) -- variance peak proxy for critical point."""
    if not stds:
        return None
    idx = max(range(len(stds)), key=lambda i: stds[i])
    return bdps[idx]
