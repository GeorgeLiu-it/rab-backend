# RAG using Ollama and Python

## Backend stack

Fastapi

## Chat model

deepseek-r1:7b

## Embedding model

deepseek-r1:7b

## Create PGSQL using docker

```bash
docker run -d \
  --name pgvector \
  -e POSTGRES_DB=rag_vector \
  -e POSTGRES_USER=george \
  -e POSTGRES_PASSWORD=123456 \
  -v pgdata2:/var/lib/postgresql/data \
  -p 5433:5432 \
  ankane/pgvector:latest
```

## PGSQL table test

[http://localhost:8000/test/check_index?table_name=langchain_pg_collection&column_name=uuid](http://localhost:8000/test/check_index?table_name=langchain_pg_collection&column_name=uuid)

## JSON format for /local/embed post request to FastAPI

```json
{
    "filepath": "/path/to/file",
    "filename": "example.txt",
    "file_content_type": "text/plain",
    "file_id": "12345"
}
```

## Generate JWT token

python .\tests\jwt_auth.py

**365 days token**
{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3R1c2VyIiwiZXhwIjoxNzgxMTQwMTE5fQ.Ko4AvBorwmrY1nT_PtY4qkG7LG81qjplzSimwmlqIO8'}

## Local embedding

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
