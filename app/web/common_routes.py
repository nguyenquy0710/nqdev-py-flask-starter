from flask import render_template, request, redirect, flash, url_for
import pandas as pd

from . import web_bp
from app.db.auth_handler import validate_session_token
from app.db.sqlite_handler import get_all_symbols, add_symbol, delete_symbol, get_symbol_info_all
from app.helpers.logging_helper import LoggingHelper


@web_bp.route("/")
def index():
    """Trang chủ - chỉ cho phép user đã đăng nhập"""
    session_token = request.cookies.get('session_token')

    if not session_token:
        # Chưa đăng nhập -> redirect to login
        return redirect(url_for('web.login'))

    user = validate_session_token(session_token)
    if not user:
        # Token không hợp lệ -> clear cookie và redirect to login
        flash('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại', 'warning')
        response = redirect(url_for('web.login'))
        response.set_cookie('session_token', '', expires=0, path='/')
        return response

    # Đã đăng nhập -> hiển thị dashboard
    return dashboard()


@web_bp.route("/dashboard")
def dashboard():
    """Dashboard chính cho user đã đăng nhập"""
    symbols = get_all_symbols()
    symbol_info = get_symbol_info_all()
    prices = {s: "-" for s in symbols}
    actual_profit = {}
    first_symbol = symbols[0] if symbols else None

    LoggingHelper.log_http_access(request.method, request.path, 200)
    return render_template("index.html", prices=prices, symbol_info=symbol_info, actual_profit=actual_profit, first_symbol=first_symbol)
