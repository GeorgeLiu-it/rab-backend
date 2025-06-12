# main.py
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from starlette.responses import JSONResponse

from app.core.config import VectorDBType, debug_mode, RAG_HOST, RAG_PORT, CHUNK_SIZE, CHUNK_OVERLAP, PDF_EXTRACT_IMAGES, VECTOR_DB_TYPE, \
    LogMiddleware, logger
from app.core.middleware import security_middleware
from app.crud.base import create_db_and_tables
from app.routers import document_routes, pgvector_routes
from app.db.base import PSQLDatabase, ensure_custom_id_index_on_embedding
# 导入 fastApi 子模块
from app.routers import chat_router
from app.routers import chat_session_router
from app.routers import document_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic goes here
    if VECTOR_DB_TYPE == VectorDBType.PGVECTOR:
        await PSQLDatabase.get_pool()  # Initialize the pool
        await ensure_custom_id_index_on_embedding()
    yield

app = FastAPI(lifespan=lifespan, debug=debug_mode)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LogMiddleware)

app.middleware("http")(security_middleware)

# Set state variables for use in routes
app.state.CHUNK_SIZE = CHUNK_SIZE
app.state.CHUNK_OVERLAP = CHUNK_OVERLAP
app.state.PDF_EXTRACT_IMAGES = PDF_EXTRACT_IMAGES

# Include routers
app.include_router(document_routes.router)
app.include_router(chat_router.router)
app.include_router(chat_session_router.router)
app.include_router(document_router.router)
if debug_mode:
    app.include_router(router=pgvector_routes.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    logger.debug(f"Validation error occurred")
    logger.debug(f"Raw request body: {body.decode()}")
    logger.debug(f"Validation errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": body.decode(),
            "message": "Request validation failed",
        },
    )

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host=RAG_HOST, port=RAG_PORT, log_config=None)
