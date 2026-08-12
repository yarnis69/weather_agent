FROM python:3.13-slim

# Install Node.js for the MCP subprocess (npx)
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV GOOGLE_GENAI_USE_VERTEXAI="False"

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080"]