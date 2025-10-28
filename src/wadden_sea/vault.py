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
    """
    Vault is a utility class for securely retrieving secrets from Azure Key Vault, with a fallback to environment variables.
    This class handles authentication with Azure Key Vault using DefaultAzureCredential and provides convenient properties
    for accessing commonly used secrets such as deployment endpoints, API keys, and database credentials. If a secret is not
    found in Azure Key Vault, it attempts to retrieve it from environment variables, ensuring robust secret management for
    various deployment scenarios.
    Attributes:
        credential (DefaultAzureCredential): The Azure credential used for authentication.
        client (SecretClient): The client used to interact with Azure Key Vault.
    Methods:
        get_secret(secret_name: str) -> str:
            Retrieves the value of a secret by its name from Azure Key Vault or environment variables.
    Properties:
        deployment_endpoint (str): The deployment endpoint for LLM base models.
        llm_key (str): The deployment key for the LLM base model.
        embedding_key (str): The deployment key for the embedding model.
        embedding_model (str): The embedding model name.
        cosmos_endpoint (str): The Cosmos DB endpoint.
        cosmos_key (str): The Cosmos DB API key (read/write).
        postgres_endpoint (str): The Postgres endpoint.
        postgres_password (str): The Postgres password.
        ValueError: If a requested secret is not found in both Azure Key Vault and environment variables.
    """
    
    def __init__(self, vault_url: str):
        """
        Initializes the Vault utility with the specified Azure Key Vault URL.

        Attempts to authenticate using the DefaultAzureCredential and initializes
        the SecretClient for interacting with the Azure Key Vault. Logs and raises
        an exception if authentication or client initialization fails.
        The user needs to  be logged in via Azure CLI or have appropriate environment variables set.

        Args:
            vault_url (str): The URL of the Azure Key Vault to connect to.

        Raises:
            Exception: If authentication or SecretClient initialization fails.
        """
        self.vault_url = vault_url
        try:
            self.credential = DefaultAzureCredential()
            self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
        except Exception as e:
            logging.error(f"Failed to authenticate or initialize SecretClient: {e}")
            raise

    def get_secret(self, secret_name: str):
        """
        Retrieve a secret value by its name from Azure Key Vault. 
        If the secret is not found in the vault, attempts to retrieve it from environment variables.

        Args:
            secret_name (str): The name of the secret to retrieve.

        Returns:
            str: The value of the secret.

        Raises:
            ValueError: If the secret is not found in both Azure Key Vault and environment variables.
        """
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except (ResourceNotFoundError, HttpResponseError) as e:
            logging.warning(f"Secret not found in the Azure vault; trying in environment variables. Details: {e}")
            env = os.environ.get(secret_name)
            if not env:
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
