from app.config import Config
from app.db.auth_handler import init_auth_db, set_db_path as set_auth_path
from app.db.sqlite_handler import init_sqlite_db, set_db_path as set_sqlite_path


def init_app_db():
    """Create a new database"""

    set_sqlite_path(path=Config.DB_PATH)
    init_sqlite_db()

    set_auth_path(path=Config.DB_PATH)
    init_auth_db()
