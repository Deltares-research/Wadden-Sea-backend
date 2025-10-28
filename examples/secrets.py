from wadden_sea.vault import Vault

uri = "https://wadden-sea-vault.vault.azure.net/"
vault = Vault(uri)
print(vault.embedding_model)