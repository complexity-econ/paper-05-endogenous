#!/usr/bin/env bash
# Paper-05: Endogenous Sigma + Dynamic Network — Master Orchestrator
# Total: 2,520 + 3,780 + 3,780 = 10,080 simulations
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================================"
echo "Paper-05: Endogenous Sigma + Dynamic Network (Factorial Design)"
echo "Total budget: 10,080 simulations (30 seeds each)"
echo "================================================================"
echo "Start time: $(date)"
echo ""

echo ">>> Campaign 1: 2x2 Factorial Core (2,520 sims)"
bash "${SCRIPT_DIR}/run_campaign1_factorial.sh"
echo "Campaign 1 done at $(date)"
echo ""

echo ">>> Campaign 2: Lambda Sensitivity (3,780 sims)"
bash "${SCRIPT_DIR}/run_campaign2_lambda.sh"
echo "Campaign 2 done at $(date)"
echo ""

echo ">>> Campaign 3: Rho Sensitivity (3,780 sims)"
bash "${SCRIPT_DIR}/run_campaign3_rho.sh"
echo "Campaign 3 done at $(date)"
echo ""

echo "================================================================"
echo "All campaigns complete. End time: $(date)"
echo "================================================================"
