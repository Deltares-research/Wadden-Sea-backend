#!/usr/bin/env bash
set -euo pipefail

RG_NAME="${RG_NAME:-wadden-sea}"
ACR_NAME="${ACR_NAME:-waddencr}"

az deployment group create --resource-group "$RG_NAME" \
     --template-file infra/azure-deploy.bicep \
     --parameters containerImage='waddencr.azurecr.io/vfn-rag:latest' \
                  acrName="$ACR_NAME" \
                  acrUsername="$ACR_NAME" \
                  acrPassword='in the vault' \
                  postgresAdminPassword='in the vault'