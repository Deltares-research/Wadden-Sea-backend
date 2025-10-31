# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Configure Poetry
RUN poetry config virtualenvs.create false

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Copy application code
COPY . .

# Install all dependencies including the llm group and the package itself
RUN poetry install --with vfn_rag --no-interaction

# Expose port 80
EXPOSE 80

# Run the application
CMD ["python", "app.py"]
