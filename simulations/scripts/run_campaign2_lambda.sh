#!/usr/bin/env bash
# Campaign 2: Lambda Sensitivity
# Fixed: rho=0 (static network). Sweep lambda in {0, 0.005, 0.01, 0.02, 0.05, 0.1}
# 6 lambda values x 21 BDP levels x 30 seeds = 3,780 simulations
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
JAR="${PAPER_DIR}/../core/target/scala-3.5.2/sfc-abm.jar"
RESULTS_DIR="${PAPER_DIR}/simulations/results/c2_lambda"
SEEDS=30

if [ ! -f "$JAR" ]; then
  echo "ERROR: JAR not found at $JAR"
  echo "Run: cd core && sbt assembly"
  exit 1
fi

BDP_LEVELS=(0 250 500 750 1000 1250 1500 1750 2000 2250 2500 2750 3000 3250 3500 3750 4000 4250 4500 4750 5000)
LAMBDAS=(0 0.005 0.01 0.02 0.05 0.1)

mkdir -p "$RESULTS_DIR"

echo "======================================================"
echo "Campaign 2: Lambda Sensitivity (${#LAMBDAS[@]} x ${#BDP_LEVELS[@]} x ${SEEDS} = $((${#LAMBDAS[@]} * ${#BDP_LEVELS[@]} * SEEDS)) sims)"
echo "======================================================"

for lambda in "${LAMBDAS[@]}"; do
  lambda_safe="${lambda//./_}"
  echo ""
  echo "--- Lambda=${lambda} ---"

  for bdp in "${BDP_LEVELS[@]}"; do
    prefix="c2_lam${lambda_safe}_bdp${bdp}"
    echo "  BDP=${bdp} ..."
    SIGMA_LAMBDA="${lambda}" REWIRE_RHO=0 TOPOLOGY=ws FIRMS_COUNT=10000 \
      java -jar "$JAR" "$bdp" "$SEEDS" "$prefix" pln

    mv "mc/${prefix}_terminal.csv" "$RESULTS_DIR/"
    rm -f "mc/${prefix}_timeseries.csv"
  done
done

echo ""
echo "Campaign 2 complete."
