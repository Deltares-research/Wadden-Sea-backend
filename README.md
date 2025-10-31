# Dependencies
- LLM related functionalities [vfn-rag](https://github.com/Deltares-research/vfn-rag)
- [Wadden-Sea-vfn](https://github.com/Deltares-research/Wadden-Sea-vfn)


## Run the FastAPI Application

### Method 1: Using Poetry (Recommended)
```bash
# Install dependencies first
poetry install

# Run the FastAPI app
poetry run python app.py
```

### Method 2: Using Poetry with uvicorn directly
```bash
# Run with uvicorn for better performance
poetry run uvicorn app:app --host 0.0.0.0 --port 80 --reload
```

### Method 3: Using CLI commands
```bash
# Test CLI commands
poetry run wadden-sea hello
poetry run wadden-sea version
poetry run wadden-sea query --query "test query"
```

## API Endpoints

Once the FastAPI app is running, you can access:

- **API Documentation:** http://localhost:80/docs

- Open http://localhost:80/docs for interactive API documentation
- Click "Try it out" on any endpoint to test it



### Prerequisites

Before running with Docker Compose, ensure you have all required environment variables set. You can either:

1. **Create a `.env` file** in the project root with all variables:
   ```bash
   # Azure Cosmos DB
   AZURE_COSMOSDB_URI=your-cosmos-uri
   AZURE_COSMOSDB_KEY=your-cosmos-key
   
   # Azure OpenAI (shared)
   AZURE_OPENAI_BASE=your-openai-endpoint
   AZURE_OPENAI_KEY=your-openai-key
   AZURE_OPENAI_VERSION=your-api-version
   
   # Azure OpenAI LLM
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   AZURE_OPENAI_MODEL=your-model-name
   
   # Azure OpenAI Embeddings
   AZURE_OPENAI_EMBEDDING_MODEL=your-embedding-model
   AZURE_EMBED_DEPLOYMENT_NAME=your-embed-deployment-name
   ```


### Build and Run with Docker Compose

```bash
# Build and start the container in detached mode
docker-compose up -d
```

### Rebuild After Code Changes

```bash
# Rebuild the image and restart containers
docker-compose up -d --build
```


### Stop and Remove Containers

```bash
# Stop containers
docker-compose down



### Required Environment Variables

The following environment variables are required for the application to function:

**Azure Cosmos DB:**
- `AZURE_COSMOSDB_URI` - Your Azure Cosmos DB account URI
- `AZURE_COSMOSDB_KEY` - Your Azure Cosmos DB account key

**Azure OpenAI:**
- `AZURE_OPENAI_BASE` - Your Azure OpenAI endpoint
- `AZURE_OPENAI_KEY` - Your Azure OpenAI API key
- `AZURE_OPENAI_VERSION` - API version

**Azure OpenAI LLM:**
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Deployment name for the LLM
- `AZURE_OPENAI_MODEL` - Model name 

**Azure OpenAI Embeddings:**
- `AZURE_OPENAI_EMBEDDING_MODEL` - Embedding model name
- `AZURE_EMBED_DEPLOYMENT_NAME` - Deployment name for embeddings
