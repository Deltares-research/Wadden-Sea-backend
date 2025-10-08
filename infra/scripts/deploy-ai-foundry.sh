#!/usr/bin/env bash
set -euo pipefail

RG_NAME="${RG_NAME:-wadden-sea}"
LOCATION="${LOCATION:-francecentral}"

# create resource group
#az group create --name "$RG_NAME" --location "$LOCATION"

# create deployment
az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file infra/ai-foundry.bicep \
  --verbose --debug

