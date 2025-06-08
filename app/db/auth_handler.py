# app/db/auth_handler.py
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt

from app.config import Config, logger

_current_db_path = Config.DB_PATH or "app/data/auth.db"  # dùng mặc định


def set_db_path(path):
    global _current_db_path
    _current_db_path = path


def init_auth_db():
    """Khởi tạo database cho authentication"""
    conn = sqlite3.connect(_current_db_path)
    cursor = conn.cursor()

    # Bảng users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            full_name TEXT,
            avatar_url TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bảng zalo_users cho OAuth
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zalo_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            zalo_id TEXT UNIQUE NOT NULL,
            zalo_name TEXT,
            zalo_avatar TEXT,
            access_token TEXT,
            refresh_token TEXT,
            token_expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Bảng sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS set_updated_at
        AFTER UPDATE ON users
        FOR EACH ROW
        BEGIN
            UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
        END;
    """)

    conn.commit()
    conn.close()
    logger.info("Auth database initialized successfully")


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{pwd_hash}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        salt, pwd_hash = hashed_password.split(':')
        return hashlib.sha256((password + salt).encode()).hexdigest() == pwd_hash
    except:
        return False


def create_user(email: str, password: str, full_name: str = None, avatar_url: str = None) -> Optional[int]:
    """Tạo user mới với email/password"""
    try:
        conn = sqlite3.connect(_current_db_path)
        cursor = conn.cursor()

        password_hash = hash_password(password)

        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, avatar_url)
            VALUES (?, ?, ?, ?)
        """, (email, password_hash, full_name, avatar_url))

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"User created successfully: {email}")
        return user_id
    except sqlite3.IntegrityError:
        logger.error(f"User already exists: {email}")
        return None
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Xác thực user bằng email/password"""
    try:
        conn = sqlite3.connect(_current_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE email = ? AND is_active = 1
        """, (email,))

        user = cursor.fetchone()
        conn.close()

        if user and verify_password(password, user['password_hash']):
            return dict(user)
        return None
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        return None


def create_zalo_user(zalo_id: str, zalo_name: str, zalo_avatar: str,
                     access_token: str, refresh_token: str, expires_in: int) -> Optional[int]:
    """Tạo hoặc cập nhật user từ Zalo OAuth"""
    try:
        conn = sqlite3.connect(_current_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Kiểm tra user đã tồn tại chưa
        cursor.execute(
            "SELECT * FROM zalo_users WHERE zalo_id = ?", (zalo_id,))
        existing_zalo_user = cursor.fetchone()

        expires_at = datetime.now() + timedelta(seconds=expires_in)

        if existing_zalo_user:
            # Cập nhật thông tin
            cursor.execute("""
                UPDATE zalo_users SET
                    zalo_name = ?, zalo_avatar = ?, access_token = ?,
                    refresh_token = ?, token_expires_at = ?
                WHERE zalo_id = ?
            """, (zalo_name, zalo_avatar, access_token, refresh_token, expires_at, zalo_id))

            user_id = existing_zalo_user['user_id']
        else:
            # Tạo user mới trong bảng users
            cursor.execute("""
                INSERT INTO users (email, full_name, avatar_url)
                VALUES (?, ?, ?)
            """, (f"{zalo_id}@zalo.me", zalo_name, zalo_avatar))

            user_id = cursor.lastrowid

            # Tạo zalo_user
            cursor.execute("""
                INSERT INTO zalo_users (user_id, zalo_id, zalo_name, zalo_avatar,
                                      access_token, refresh_token, token_expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, zalo_id, zalo_name, zalo_avatar, access_token, refresh_token, expires_at))

        conn.commit()
        conn.close()

        logger.info(f"Zalo user created/updated: {zalo_id}")
        return user_id
    except Exception as e:
        logger.error(f"Error creating Zalo user: {e}")
        return None


def create_session_token(user_id: int) -> str:
    """Tạo session token cho user"""
    try:
        conn = sqlite3.connect(_current_db_path)
        cursor = conn.cursor()

        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=30)  # Token valid for 30 days

        cursor.execute("""
            INSERT INTO user_sessions (user_id, session_token, expires_at)
            VALUES (?, ?, ?)
        """, (user_id, session_token, expires_at))

        conn.commit()
        conn.close()

        return session_token
    except Exception as e:
        logger.error(f"Error creating session token: {e}")
        return None


def validate_session_token(session_token: str) -> Optional[Dict[str, Any]]:
    """Validate session token và trả về user info"""
    try:
        conn = sqlite3.connect(_current_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.*, s.expires_at FROM users u
            JOIN user_sessions s ON u.id = s.user_id
            WHERE s.session_token = ? AND s.expires_at > ? AND u.is_active = 1
        """, (session_token, datetime.now()))

        user = cursor.fetchone()
        conn.close()

        if user:
            return dict(user)
        return None
    except Exception as e:
        logger.error(f"Error validating session token: {e}")
        return None


def revoke_session_token(session_token: str) -> bool:
    """Revoke (xóa) session token"""
    try:
        conn = sqlite3.connect(_current_db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM user_sessions WHERE session_token = ?", (session_token,))

        conn.commit()
        conn.close()

        return True
    except Exception as e:
        logger.error(f"Error revoking session token: {e}")
        return False


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Lấy thông tin user by ID"""
    try:
        conn = sqlite3.connect(_current_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id = ? AND is_active = 1", (user_id,))
        user = cursor.fetchone()
        conn.close()

        # Convert datetime to ISO format before returning
        if user and 'created_at' in user:
            if isinstance(user['created_at'], str):
                # Parse string datetime and convert to ISO format
                try:
                    dt = datetime.strptime(
                        user['created_at'], '%Y-%m-%d %H:%M:%S')
                    user['created_at'] = dt.isoformat()
                except:
                    pass

        if user:
            return dict(user)
        return None
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None
