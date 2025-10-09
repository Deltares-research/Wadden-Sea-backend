from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class Vault:
    def __init__(self, vault_url: str):
        self.vault_url = vault_url
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_name: str):
        secret = self.client.get_secret(secret_name)
        return secret.value
    
    @property
    def deployment_endpoint(self):
        """Get the deployment endpoint for the LLM base models (llm and embedding) from Azure Key Vault"""
        return self.get_secret("LLM-BASE-GPT-4o-ENDPOINT")
    
    
    @property
    def llm_key(self):
        """Get the deployment key for the LLM base model from Azure Key Vault"""
        return self.get_secret("LLM-BASE-GPT-4o-KEY")
    
    @property
    def embedding_key(self):
        """Get the deployment key for the embedding model from Azure Key Vault"""
        return self.get_secret("Embedding-3-large-KEY")
    
    @property
    def embedding_model(self):  
        """Get the embedding model name from Azure Key Vault"""
        return self.get_secret("EMBEDDING-MODEL")
    
    @property
    def cosmos_endpoint(self):
        """Get the Cosmos DB endpoint from Azure Key Vault"""
        return self.get_secret("COSMOS-ENDPOINT")
    
    @property
    def cosmos_key(self):
        """Get the Cosmos DB API key (read/write) from Azure Key Vault"""
        return self.get_secret("COSMOS-API-KEY-READ-WRITE")
    
    @property
    def postgres_endpoint(self):
        """Get the Postgres endpoint from Azure Key Vault"""
        return self.get_secret("POSTGRES-ENDPOINT")
    
    @property
    def postgres_password(self):
        """Get the Postgres password from Azure Key Vault"""
        return self.get_secret("POSTGRES-PASSWORD")

    
