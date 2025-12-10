from psycopg import connect
from psycopg.rows import dict_row
from .config import settings


def get_db_connection():
    return connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        row_factory=dict_row
    )
