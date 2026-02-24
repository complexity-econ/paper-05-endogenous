#!/usr/bin/env bash
# Campaign 3: Rho Sensitivity
# Fixed: lambda=0 (static sigma). Sweep rho in {0, 0.02, 0.05, 0.1, 0.2, 0.5}
# 6 rho values x 21 BDP levels x 30 seeds = 3,780 simulations
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
JAR="${PAPER_DIR}/../core/target/scala-3.5.2/sfc-abm.jar"
RESULTS_DIR="${PAPER_DIR}/simulations/results/c3_rho"
SEEDS=30

if [ ! -f "$JAR" ]; then
  echo "ERROR: JAR not found at $JAR"
  echo "Run: cd core && sbt assembly"
  exit 1
fi

BDP_LEVELS=(0 250 500 750 1000 1250 1500 1750 2000 2250 2500 2750 3000 3250 3500 3750 4000 4250 4500 4750 5000)
RHOS=(0 0.02 0.05 0.1 0.2 0.5)

mkdir -p "$RESULTS_DIR"

echo "======================================================"
echo "Campaign 3: Rho Sensitivity (${#RHOS[@]} x ${#BDP_LEVELS[@]} x ${SEEDS} = $((${#RHOS[@]} * ${#BDP_LEVELS[@]} * SEEDS)) sims)"
echo "======================================================"

for rho in "${RHOS[@]}"; do
  rho_safe="${rho//./_}"
  echo ""
  echo "--- Rho=${rho} ---"

  for bdp in "${BDP_LEVELS[@]}"; do
    prefix="c3_rho${rho_safe}_bdp${bdp}"
    echo "  BDP=${bdp} ..."
    SIGMA_LAMBDA=0 REWIRE_RHO="${rho}" TOPOLOGY=ws FIRMS_COUNT=10000 \
      java -jar "$JAR" "$bdp" "$SEEDS" "$prefix" pln

    mv "mc/${prefix}_terminal.csv" "$RESULTS_DIR/"
    rm -f "mc/${prefix}_timeseries.csv"
  done
done

echo ""
echo "Campaign 3 complete."
