# app/utils/health.py
from app.core.config import VECTOR_DB_TYPE, VectorDBType
from app.db.base import pg_health_check


def is_health_ok():
    if VECTOR_DB_TYPE == VectorDBType.PGVECTOR:
        return pg_health_check()
    else:
        return True