from flask import request, redirect, flash, url_for
from functools import wraps

from app.db.auth_handler import validate_session_token

# Authentication decorator


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for session token in cookies or header
        session_token = request.cookies.get('session_token')
        if not session_token:
            session_token = request.headers.get('Authorization')
            if session_token and session_token.startswith('Bearer '):
                session_token = session_token[7:]
        if not session_token:
            flash('Vui lòng đăng nhập để tiếp tục', 'warning')
            return redirect(url_for('web.login'))
        user = validate_session_token(session_token)
        if not user:
            flash('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại', 'warning')
            return redirect(url_for('web.login'))
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function
