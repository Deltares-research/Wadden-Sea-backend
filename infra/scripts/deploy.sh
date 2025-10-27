#!/usr/bin/env bash
set -euo pipefail
# variables with default values
RG_NAME="${RG_NAME:-wadden-sea}"
ACR_NAME="${ACR_NAME:-waddencr}"
VAULT_NAME="${VAULT_NAME:-wadden-sea-vault}"

# secret names with default values
ACR_PASSWORD_SECRET_NAME="${ACR_PASSWORD_SECRET_NAME:-CONTAINER-REGISTRY-PASSWORD}"
POSTGRES_PASSWORD_SECRET_NAME="${POSTGRES_PASSWORD_SECRET_NAME:-POSTGRES-PASSWORD}"
LLM_API_KEY_NAME="${LLM_API_KEY_NAME:-LLM-BASE-GPT-4o-KEY}"


echo "🔐 Retrieving secrets from Key Vault: $VAULT_NAME"

# Retrieve secrets from Azure Key Vault
echo "  - Retrieving ACR password..."
ACR_PASSWORD=$(az keyvault secret show --vault-name "$VAULT_NAME" --name "$ACR_PASSWORD_SECRET_NAME" --query value -o tsv)

echo "  - Retrieving PostgreSQL password..."
POSTGRES_PASSWORD=$(az keyvault secret show --vault-name "$VAULT_NAME" --name "$POSTGRES_PASSWORD_SECRET_NAME" --query value -o tsv)

echo "  - Retrieving API key..."
API_KEY=$(az keyvault secret show --vault-name "$VAULT_NAME" --name "$LLM_API_KEY_NAME" --query value -o tsv)

echo "✅ All secrets retrieved successfully"

echo "🚀 Starting deployment..."
az deployment group create \
    --resource-group "$RG_NAME" \
    --template-file infra/azure-deploy.bicep \
    --parameters acrName="$ACR_NAME" \
                 acrUsername="$ACR_NAME" \
                 acrPassword="$ACR_PASSWORD" \
                 postgresAdminPassword="$POSTGRES_PASSWORD" \
                 apiKey="$API_KEY" \
    --verbose --debug