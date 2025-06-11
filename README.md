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
