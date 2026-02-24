# Paper 05: Endogenous Technology and Network Dynamics in AI Adoption

**A Factorial Agent-Based Study**

Fifth paper in the [complexity-econ](https://github.com/complexity-econ) series. Tests whether the universality of AI adoption phase transitions (established in [Paper 04](https://github.com/complexity-econ/paper-04-phase-diagram)) survives when both the sectoral elasticity of substitution (σ) and the inter-firm network are made endogenous.

## Key Findings

- The **reentrant (inverted-U) adoption shape** survives in all four factorial cells
- Endogenous σ preserves BDP_c = 500 PLN up to moderate learning rates (λ ≤ 0.02)
- Dynamic network rewiring shifts BDP_c to 750 PLN for intermediate rates (ρ ∈ [0.02, 0.10])
- The combined effect is **superadditive** (+6.5 pp peak adoption vs. baseline)
- Endogenous σ does **not** produce self-organized criticality (SOC)

## Experimental Design

2×2 factorial: (fixed/endogenous σ) × (static/dynamic network), plus two marginal sensitivity sweeps.

| Campaign | Simulations | Description |
|----------|------------|-------------|
| C1 Factorial | 2,520 | 4 cells × 21 BDP × 30 seeds |
| C2 Lambda | 3,780 | 6 λ values × 21 BDP × 30 seeds |
| C3 Rho | 3,780 | 6 ρ values × 21 BDP × 30 seeds |
| **Total** | **10,080** | |

## Repository Structure

```
analysis/python/       — 7 analysis scripts generating 12 figures
figures/               — Generated PNG figures (200 DPI)
latex/                 — Paper source (XeLaTeX + biblatex)
simulations/
  scripts/             — Campaign runner scripts
  results/             — Terminal CSV files (European format)
```

## Dependencies

- **Engine**: [complexity-econ/core](https://github.com/complexity-econ/core) (Scala 3.5.2, sbt)
- **Analysis**: Python 3 (matplotlib, numpy, pandas, seaborn)
- **Paper**: XeLaTeX + biblatex

## Running

```bash
# Run all simulation campaigns (~3h on M-series Mac)
cd simulations/scripts && bash run_all.sh

# Generate all figures
cd analysis/python && for f in factorial_bifurcation sigma_trajectories network_evolution lambda_sensitivity rho_sensitivity universality_test; do python3 ${f}.py; done

# Compile paper
cd latex && xelatex paper_en.tex && bibtex paper_en && xelatex paper_en.tex && xelatex paper_en.tex
```

## Series

| # | Paper | DOI |
|---|-------|-----|
| 01 | [The Acceleration Paradox](https://github.com/complexity-econ/paper-01-acceleration-paradox) | [10.5281/zenodo.18727928](https://doi.org/10.5281/zenodo.18727928) |
| 02 | [Monetary Regime & Automation](https://github.com/complexity-econ/paper-02-monetary-regimes) | [10.5281/zenodo.18740933](https://doi.org/10.5281/zenodo.18740933) |
| 03 | [Empirical σ Estimation](https://github.com/complexity-econ/paper-03-empirical-sigma) | [10.5281/zenodo.18743780](https://doi.org/10.5281/zenodo.18743780) |
| 04 | [Phase Diagram & Universality](https://github.com/complexity-econ/paper-04-phase-diagram) | [10.5281/zenodo.18751083](https://doi.org/10.5281/zenodo.18751083) |
| **05** | **Endogenous Technology & Networks** | *this repo* |

## License

MIT
