from typing import Dict
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError
import os
import logging

SECRET_NAMES: Dict[str, str] = {
    "deployment_endpoint": "LLM-BASE-GPT-4o-ENDPOINT",
    "llm_key": "LLM-BASE-GPT-4o-KEY",
    "embedding_key": "Embedding-3-large-KEY",
    "embedding_model": "EMBEDDING-MODEL",
    "cosmos_endpoint": "COSMOS-ENDPOINT",
    "cosmos_key": "COSMOS-API-KEY-READ-WRITE",
    "postgres_endpoint": "POSTGRES-ENDPOINT",
    "postgres_password": "POSTGRES-PASSWORD",
}

class Vault:
    def __init__(self, vault_url: str):
        self.vault_url = vault_url
        try:
            self.credential = DefaultAzureCredential()
            self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
        except Exception as e:
            logging.error(f"Failed to authenticate or initialize SecretClient: {e}")
            raise

    def get_secret(self, secret_name: str):
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except (ResourceNotFoundError, HttpResponseError) as e:
            logging.warning(f"Secret not found in the Azure vault; trying in environmental variables. Details: {e}")
            env = os.environ.get(secret_name)
            if (not env):
                raise ValueError(f"Secret '{secret_name}' not found in Azure Key Vault or environment variables.")
            return env
           

    @property
    def deployment_endpoint(self):
        """Get the deployment endpoint for the LLM base models (llm and embedding) from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["deployment_endpoint"])
    
    
    @property
    def llm_key(self):
        """Get the deployment key for the LLM base model from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["llm_key"])
    
    @property
    def embedding_key(self):
        """Get the deployment key for the embedding model from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["embedding_key"])
    
    @property
    def embedding_model(self):
        """Get the embedding model name from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["embedding_model"])
    
    @property
    def cosmos_endpoint(self):
        """Get the Cosmos DB endpoint from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["cosmos_endpoint"])
    
    @property
    def cosmos_key(self):
        """Get the Cosmos DB API key (read/write) from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["cosmos_key"])
    
    @property
    def postgres_endpoint(self):
        """Get the Postgres endpoint from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["postgres_endpoint"])
    
    @property
    def postgres_password(self):
        """Get the Postgres password from Azure Key Vault"""
        return self.get_secret(SECRET_NAMES["postgres_password"])
