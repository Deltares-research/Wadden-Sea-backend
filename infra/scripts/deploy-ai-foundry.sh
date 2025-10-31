#!/bin/bash
set -euo pipefail

RG_NAME="${RG_NAME:-wadden-sea}"
LOCATION="${LOCATION:-francecentral}"

# create deployment
az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file infra/ai-foundry.bicep \
  --verbose --debug

