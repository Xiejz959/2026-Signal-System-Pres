#!/usr/bin/env bash

set -euo pipefail

ENV_FILE="$(cd "$(dirname "$0")" && pwd)/environment_ssp_voice.yml"
ENV_NAME="ssp_voice"

echo "Creating conda environment from: $ENV_FILE"
conda env create -f "$ENV_FILE" || conda env update -f "$ENV_FILE" --prune


echo
echo "Done."
echo "Activate with: conda activate $ENV_NAME"
