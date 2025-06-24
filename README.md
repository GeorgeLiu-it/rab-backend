# Fastapi RAG application deployment using docker

## System setup

Refert to README_env.md in server project

## Docker images

```bash
# Export
docker save -o [image.tar] [local-image:version]

# Import
docker load -i [image.tar]
```

## Application deployment

### PGVector

**Docker command**

```bash
docker run -d \
  --name pgvector \
  -e POSTGRES_DB=rag_vector \
  -e POSTGRES_USER=george \
  -e POSTGRES_PASSWORD=123456 \
  -v $HOME/postgresql/data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --restart unless-stopped \
  ankane/pgvector:latest
```

### Rag application

**Build docker image**

- Dockerfile

```dockerfile
# ---- Base image ----
FROM python:3.12.1-slim

# Add your private CA
COPY Zscaler_Root_CA.crt /usr/local/share/ca-certificates/ca.crt
RUN update-ca-certificates

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . /app/

# Expose port
EXPOSE 8000

# Command to run the app with Gunicorn and Uvicorn workers
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60"]
```

- Run

```bash
# Generate docker image
docker build -t rag_backend .

# Run docker container
docker run -d -p 8000:8000 -v $HOME/rag_backend/.env:/app/.env --name rag_backend rag_backend:latest
```

**Docker-compose to run all-in-one**

- .env.docker-compose file

- docker-compose.yml

  ```yml
  version: '3.8'
  
  services:
    rag_backend:
      build: .
      container_name: rag_backend
      depends_on:
        - db
      ports:
        - "${APP_PORT}:8000"
      environment:
        POSTGRES_DB: ${POSTGRES_DB}
        POSTGRES_USER: ${POSTGRES_USER}
        POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
        POSTGRES_HOST: db
      volumes:
        - "${HOME_DIR}/rag_backend/.env:/app/.env"
      networks:
        - rag_net
      restart: unless-stopped
  
    db:
      image: ankane/pgvector:latest
      container_name: pgvector
      environment:
        POSTGRES_DB: ${POSTGRES_DB}
        POSTGRES_USER: ${POSTGRES_USER}
        POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      volumes:
        - "${HOME_DIR}/postgresql/data:/var/lib/postgresql/data"
      ports:
        - "${POSTGRES_PORT}:5432"
      networks:
        - rag_net
      restart: unless-stopped
  
  networks:
    rag_net:
      driver: bridge
  
  ```

- Docker-compose command

  ```bash
  # up
  docker compose --env-file .env.docker-compose up -d
  
  # down
  docker compose --env-file .env.docker-compose down
  ```

## Embedding and LLM integration

### Backend stack

Fastapi

### Chat model

deepseek-r1:7b

### Embedding model

deepseek-r1:7b

### Create PGSQL using docker

```bash
docker run -d \
  --name pgvector \
  -e POSTGRES_DB=rag_vector \
  -e POSTGRES_USER=george \
  -e POSTGRES_PASSWORD=123456 \
  -v pgdata2:/var/lib/postgresql/data \
  -p 5432:5432 \
  ankane/pgvector:latest
```

### PGSQL table test

[http://localhost:8000/test/check_index?table_name=langchain_pg_collection&column_name=uuid](http://localhost:8000/test/check_index?table_name=langchain_pg_collection&column_name=uuid)

### JSON format for /local/embed post request to FastAPI

```json
{
    "filepath": "/path/to/file",
    "filename": "example.txt",
    "file_content_type": "text/plain",
    "file_id": "12345"
}
```

### Generate JWT token

python .\tests\jwt_auth.py

**365 days token**
{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3R1c2VyIiwiZXhwIjoxNzgxMTQwMTE5fQ.Ko4AvBorwmrY1nT_PtY4qkG7LG81qjplzSimwmlqIO8'}

### Local embedding

![alt text](image.png)

## API

### Chat

**method**
post

**link**
<http://127.0.0.1:8000/chat>

**headers**
authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3R1c2VyIiwiZXhwIjoxNzgxMTQwMTE5fQ.Ko4AvBorwmrY1nT_PtY4qkG7LG81qjplzSimwmlqIO8
Content-Type:application/json

**body**
{
  "model": "deepseek-r1:7b",
  "stream": true,
  "messages": {
    "role": "user",
    "content": "what's the definition of Ultra Bundle, response me using english"
  },
  "chat_session_id": "92e78ed33ff242fda9ff6c181fe3859f"
}

### embedding by folder 

**method**
get

**URI**
<http://127.0.0.1:8000/documents/vector-all>

**headers**
authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3R1c2VyIiwiZXhwIjoxNzgxMTQwMTE5fQ.Ko4AvBorwmrY1nT_PtY4qkG7LG81qjplzSimwmlqIO8

### embedding by file path

**method**
post

**link**
<http://127.0.0.1:8000/local/embed>

**headers**
authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3R1c2VyIiwiZXhwIjoxNzgxMTQwMTE5fQ.Ko4AvBorwmrY1nT_PtY4qkG7LG81qjplzSimwmlqIO8
Content-Type:application/json

**body**
{
  "filepath": "C:\\Users\\liushanshan\\Documents\\ai\\rag_ollama\\uploads\\test.txt",
  "filename": "test.txt",
  "file_content_type": "text/plain",
  "file_id": "testid1"
}

### query

**method**
post

**link**
<http://127.0.0.1:8000/query_multiple>

**headers**
authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3R1c2VyIiwiZXhwIjoxNzgxMTQwMTE5fQ.Ko4AvBorwmrY1nT_PtY4qkG7LG81qjplzSimwmlqIO8
Content-Type:application/json

**body**
{
  "query": "FFF团的吉祥物是什么",
  "file_ids": [
    "testid1",
    "testid2"
  ],
  "k": 3
}

or query
{
  "query": "FFF团的吉祥物是什么",
  "file_id": "testid1",
  "k": 4,
  "entity_id": "testuser"
}

### upload

![alt text](image-1.png)

### context

![alt text](image-2.png)

## Appendix

### Configure Ollama running WSL as 0.0.0.0 access

```bash
# edit service start daemon
sudo vim /etc/systemd/system/ollama.service

# Content
[Unit]
Description=Ollama API

[Service]
ExecStart=/usr/bin/env OLLAMA_HOST=0.0.0.0 /usr/local/bin/ollama serve
Restart=always
User=YOUR_USER

[Install]
WantedBy=default.target

# reload and restart
sudo systemctl daemon-reexec
sudo systemctl enable --now ollama
```

### Window proxy forwarding

```bash
# forward network flow to wsl
netsh interface portproxy add v4tov4 listenport=11434 listenaddress=0.0.0.0 connectport=11434 connectaddress=172.29.2.187

# check the forward settings
netsh interface portproxy show all
```

### Curl ollama api on remote pc

```bash
curl http://[windows ip]:11434
```



