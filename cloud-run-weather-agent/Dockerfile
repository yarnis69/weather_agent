FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV GOOGLE_GENAI_USE_VERTEXAI="False"

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080"]