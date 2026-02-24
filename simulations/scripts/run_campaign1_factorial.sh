#!/usr/bin/env bash
# Campaign 1: 2x2 Factorial Core
# 4 cells x 21 BDP levels x 30 seeds = 2,520 simulations
# Cells: static/static, endo/static, static/dynamic, endo/dynamic
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
JAR="${PAPER_DIR}/../core/target/scala-3.5.2/sfc-abm.jar"
RESULTS_BASE="${PAPER_DIR}/simulations/results/c1_factorial"
SEEDS=30

if [ ! -f "$JAR" ]; then
  echo "ERROR: JAR not found at $JAR"
  echo "Run: cd core && sbt assembly"
  exit 1
fi

# BDP levels: 0 to 5000 in steps of 250 (21 levels)
BDP_LEVELS=(0 250 500 750 1000 1250 1500 1750 2000 2250 2500 2750 3000 3250 3500 3750 4000 4250 4500 4750 5000)

# 2x2 factorial cells: (lambda, rho, dir_name)
declare -a CELLS=(
  "0     0     static_static"
  "0.02  0     endo_static"
  "0     0.1   static_dynamic"
  "0.02  0.1   endo_dynamic"
)

echo "======================================================"
echo "Campaign 1: 2x2 Factorial (${#CELLS[@]} x ${#BDP_LEVELS[@]} x ${SEEDS} = $((${#CELLS[@]} * ${#BDP_LEVELS[@]} * SEEDS)) sims)"
echo "======================================================"

for cell_spec in "${CELLS[@]}"; do
  read -r lambda rho dirname <<< "$cell_spec"
  outdir="${RESULTS_BASE}/${dirname}"
  mkdir -p "$outdir"
  echo ""
  echo "--- Cell: ${dirname} (lambda=${lambda}, rho=${rho}) ---"

  for bdp in "${BDP_LEVELS[@]}"; do
    prefix="c1_${dirname}_bdp${bdp}"
    echo "  BDP=${bdp} ..."
    SIGMA_LAMBDA="${lambda}" REWIRE_RHO="${rho}" TOPOLOGY=ws FIRMS_COUNT=10000 \
      java -jar "$JAR" "$bdp" "$SEEDS" "$prefix" pln

    mv "mc/${prefix}_terminal.csv" "$outdir/"
    rm -f "mc/${prefix}_timeseries.csv"
  done
done

echo ""
echo "Campaign 1 complete."
