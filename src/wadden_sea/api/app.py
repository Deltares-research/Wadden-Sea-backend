from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from wadden_sea.api.engine import load_configs

query_engine = load_configs()

# Initialize FastAPI app
app = FastAPI(
    title="VFN-RAG API",
    description="RAG (Retrieval-Augmented Generation) API for voice-for-nature project",
    version="1.0.0"
)

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    query: str

class HelloResponse(BaseModel):
    message: str
    service: str

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for container monitoring"""
    return {"status": "healthy", "service": "vfn-rag"}

# Hello world endpoint
@app.get("/hello", response_model=HelloResponse)
def hello_world():
    """Simple hello world endpoint"""
    return HelloResponse(
        message="Hello World from vfn-rag container!",
        service="vfn-rag"
    )

# RAG query endpoint (placeholder for now)
@app.post("/query", response_model=QueryResponse)
def rag_query(request: QueryRequest):
    """RAG query endpoint - placeholder implementation"""
    try:
        query_response = query_engine.query(request.query, request.max_results)
        # For now, return a mock response
        return QueryResponse(
            answer=f"Mock response for query: {query_response.response}",
            sources=["mock_source1.pdf", "mock_source2.txt"],
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "VFN-RAG API is running",
        "docs": "/docs",
        "health": "/health",
        "hello": "/hello"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
