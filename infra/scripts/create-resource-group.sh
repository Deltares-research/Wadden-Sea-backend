#!/bin/bash
set -euo pipefail

RG_NAME="${RG_NAME:-wadden-sea}"
LOCATION="${LOCATION:-francecentral}"

# create resource group
az group create --name "$RG_NAME" --location "$LOCATION"

