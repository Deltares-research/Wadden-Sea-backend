#!/usr/bin/env bash
set -euo pipefail

RG_NAME="${RG_NAME:-wadden-sea}"

# create deployment
az deployment group what-if \
  --resource-group "$RG_NAME" \
  --template-file infra/azure-deploy.bicep \
  --parameters postgresAdminPassword="in the vault!"

