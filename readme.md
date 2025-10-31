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
- **Health Check:** http://localhost:80/health
- **Hello World:** http://localhost:80/hello
- **Root:** http://localhost:80/


### Using browser:
- Open http://localhost:80/docs for interactive API documentation
- Click "Try it out" on any endpoint to test it

## Run with Docker

### Build and Run Container
```bash
# Build the Docker image and run the container
docker build -t wadden-sea . && docker run -p 80:80 wadden-sea
```

### Alternative: Build and Run Separately
```bash
# Build the Docker image
docker build -t wadden-sea .

# Run the container
docker run -p 80:80 wadden-sea
```

### Test the Container
Once the container is running, test the endpoints:
- **API Documentation:** http://localhost:80/docs
- **Health Check:** http://localhost:80/health
- **Hello World:** http://localhost:80/hello

### Stop the Container
```bash
# Stop the running container
docker stop $(docker ps -q --filter ancestor=wadden-sea)
```