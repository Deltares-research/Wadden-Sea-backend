#!/usr/bin/env bash
set -euo pipefail

RG_NAME="${RG_NAME:-waddensea}"

# create deployment
az deployment group what-if \
  --resource-group "$RG_NAME" \
  --template-file infra/azure-deploy.bicep \
  --parameters postgresAdminPassword="YourSecurePassword123!"

