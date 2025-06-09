from flask import render_template, request, redirect, flash, url_for

from . import web_bp
from app.db.auth_handler import validate_session_token
from app.helpers.logging_helper import LoggingHelper


@web_bp.route("/login")
def login():
    """Trang đăng nhập"""
    # Check if user is already logged in
    session_token = request.cookies.get('session_token')
    if session_token:
        user = validate_session_token(session_token)
        if user:
            return redirect(url_for('web.index'))

    LoggingHelper.log_http_access(request.method, request.path, 200)
    return render_template("login.html")


@web_bp.route("/register")
def register():
    """Trang đăng ký"""
    # Check if user is already logged in
    session_token = request.cookies.get('session_token')
    if session_token:
        user = validate_session_token(session_token)
        if user:
            return redirect(url_for('web.index'))

    LoggingHelper.log_http_access(request.method, request.path, 200)
    return render_template("register.html")


@web_bp.route("/logout")
def logout():
    """Đăng xuất"""
    from app.db.auth_handler import revoke_session_token

    session_token = request.cookies.get('session_token')
    if session_token:
        revoke_session_token(session_token)

    flash('Đã đăng xuất thành công', 'success')
    LoggingHelper.log_http_access(request.method, request.path, 200)

    # Create response and clear the cookie
    response = redirect(url_for('web.login'))
    response.set_cookie('session_token', '', expires=0, path='/')
    return response
