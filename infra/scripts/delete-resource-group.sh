#!/bin/bash
RG_NAME="${RG_NAME:-wadden-sea}"

az group delete --name "$RG_NAME"