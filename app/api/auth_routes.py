# app/api/auth_routes.py
from flask import request, jsonify, session, redirect, url_for
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Unauthorized
import requests
import secrets
import urllib.parse
from functools import wraps

from . import api_bp, api, api_error_model
from app.config import Config, logger
from app.db.auth_handler import (
    create_user, authenticate_user, create_zalo_user,
    create_session_token, validate_session_token, revoke_session_token,
    get_user_by_id
)
from app.helpers.common_helper import format_datetime_for_api

# Zalo OAuth Configuration
ZALO_APP_ID = Config.ZALO_APP_ID
ZALO_APP_SECRET = Config.ZALO_APP_SECRET
ZALO_REDIRECT_URI = Config.ZALO_REDIRECT_URI

# Models for Swagger
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email đăng nhập'),
    'password': fields.String(required=True, description='Mật khẩu')
})

register_model = api.model('Register', {
    'email': fields.String(required=True, description='Email đăng ký'),
    'password': fields.String(required=True, description='Mật khẩu (tối thiểu 6 ký tự)'),
    'full_name': fields.String(description='Họ và tên')
})

user_model = api.model('User', {
    'id': fields.Integer(description='User ID'),
    'email': fields.String(description='Email'),
    'full_name': fields.String(description='Họ và tên'),
    'avatar_url': fields.String(description='URL avatar'),
    'is_active': fields.Boolean,
    'created_at': fields.String(description='Ngày tạo tài khoản'),
    'updated_at': fields.String(description='Ngày cập nhật tài khoản'),
})

auth_response_model = api.model('AuthResponse', {
    'success': fields.Boolean(description='Trạng thái thành công'),
    'message': fields.String(description='Thông báo'),
    'user': fields.Nested(user_model, description='Thông tin user'),
    'session_token': fields.String(description='Session token'),
    'redirect_url': fields.String(description='URL redirect (cho Zalo OAuth)')
})


# Decorator để check authentication
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = request.headers.get('Authorization')
        if session_token and session_token.startswith('Bearer '):
            session_token = session_token[7:]  # Remove 'Bearer ' prefix

        if not session_token:
            session_token = request.cookies.get('session_token')

        if not session_token:
            api.abort(401, "Missing authentication token")

        user = validate_session_token(session_token)
        if not user:
            api.abort(401, "Invalid or expired token")

        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function


# Namespace cho Auth API
ns_auth = api.namespace('auth', description='Authentication và Authorization')


@ns_auth.route('/register')
class Register(Resource):
    @ns_auth.doc('register_user')
    @ns_auth.expect(register_model)
    @ns_auth.marshal_with(auth_response_model)
    @ns_auth.response(201, 'Đăng ký thành công')
    @ns_auth.response(400, 'Dữ liệu không hợp lệ', api_error_model)
    @ns_auth.response(409, 'Email đã tồn tại', api_error_model)
    def post(self):
        """Đăng ký tài khoản mới"""
        try:
            data = request.get_json()

            # Validation
            email = data.get('email', '').strip().lower()
            password = data.get('password', '')
            full_name = data.get('full_name', '').strip()

            if not email or '@' not in email:
                api.abort(400, "Email không hợp lệ")

            if len(password) < 6:
                api.abort(400, "Mật khẩu phải có ít nhất 6 ký tự")

            # Tạo user
            user_id = create_user(email, password, full_name)
            if not user_id:
                api.abort(409, "Email đã tồn tại")

            # Tạo session token
            session_token = create_session_token(user_id)
            user = get_user_by_id(user_id)

            return {
                'success': True,
                'message': 'Đăng ký thành công',
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'avatar_url': user['avatar_url'],
                    'created_at': format_datetime_for_api(user['created_at'])
                },
                'session_token': session_token
            }, 201

        except Exception as e:
            logger.error(f"Registration error: {e}")
            api.abort(500, f"Lỗi đăng ký: {str(e)}")


@ns_auth.route('/login')
class Login(Resource):
    @ns_auth.doc('login_user')
    @ns_auth.expect(login_model)
    @ns_auth.marshal_with(auth_response_model)
    @ns_auth.response(200, 'Đăng nhập thành công')
    @ns_auth.response(401, 'Email hoặc mật khẩu không đúng', api_error_model)
    def post(self):
        """Đăng nhập bằng email và mật khẩu"""
        try:
            data = request.get_json()

            email = data.get('email', '').strip().lower()
            password = data.get('password', '')

            if not email or not password:
                api.abort(400, "Email và mật khẩu không được để trống")

            # Xác thực user
            user = authenticate_user(email, password)
            if not user:
                api.abort(401, "Email hoặc mật khẩu không đúng")

            # Tạo session token
            session_token = create_session_token(user['id'])

            return {
                'success': True,
                'message': 'Đăng nhập thành công',
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'avatar_url': user['avatar_url'],
                    # Format datetime
                    'created_at': format_datetime_for_api(user['created_at'])
                },
                'session_token': session_token
            }, 200

        except Exception as e:
            logger.error(f"Login error: {e}")
            api.abort(500, f"Lỗi đăng nhập: {str(e)}")


@ns_auth.route('/logout')
class Logout(Resource):
    @ns_auth.doc('logout_user')
    @ns_auth.response(200, 'Đăng xuất thành công')
    @auth_required
    def post(self):
        """Đăng xuất (revoke session token)"""
        try:
            session_token = request.headers.get(
                'Authorization', '').replace('Bearer ', '')
            if not session_token:
                session_token = request.cookies.get('session_token')

            if session_token:
                revoke_session_token(session_token)

            return {
                'success': True,
                'message': 'Đăng xuất thành công'
            }, 200

        except Exception as e:
            logger.error(f"Logout error: {e}")
            api.abort(500, f"Lỗi đăng xuất: {str(e)}")


@ns_auth.route('/profile')
class Profile(Resource):
    @ns_auth.doc('get_user_profile')
    @ns_auth.marshal_with(user_model)
    @ns_auth.response(200, 'Thành công')
    @auth_required
    def get(self):
        """Lấy thông tin profile của user đang đăng nhập"""
        user = request.current_user
        return {
            'id': user['id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'avatar_url': user['avatar_url'],
            'created_at': format_datetime_for_api(user['created_at'])
        }, 200

# Zalo OAuth Routes


@ns_auth.route('/zalo/login')
class ZaloLogin(Resource):
    @ns_auth.doc('zalo_oauth_login')
    @ns_auth.marshal_with(auth_response_model)
    @ns_auth.response(200, 'URL redirect để đăng nhập Zalo')
    def get(self):
        """Tạo URL để đăng nhập qua Zalo OAuth"""
        try:
            # Tạo state parameter để chống CSRF
            state = secrets.token_urlsafe(32)
            session['oauth_state'] = state

            # Tạo authorization URL
            auth_url = "https://oauth.zaloapp.com/v4/permission"
            params = {
                'app_id': ZALO_APP_ID,
                'redirect_uri': ZALO_REDIRECT_URI,
                'state': state
            }

            redirect_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

            return {
                'success': True,
                'message': 'Redirect to Zalo OAuth',
                'redirect_url': redirect_url
            }, 200

        except Exception as e:
            logger.error(f"Zalo login error: {e}")
            api.abort(500, f"Lỗi tạo URL Zalo login: {str(e)}")


@ns_auth.route('/zalo/callback')
class ZaloCallback(Resource):
    @ns_auth.doc('zalo_oauth_callback')
    @ns_auth.marshal_with(auth_response_model)
    @ns_auth.response(200, 'Đăng nhập Zalo thành công')
    @ns_auth.response(400, 'Lỗi OAuth callback', api_error_model)
    def get(self):
        """Xử lý callback từ Zalo OAuth"""
        try:
            code = request.args.get('code')
            state = request.args.get('state')

            # Verify state parameter
            if not state or state != session.get('oauth_state'):
                api.abort(400, "Invalid state parameter")

            if not code:
                api.abort(400, "Missing authorization code")

            # Exchange code for access token
            token_url = "https://oauth.zaloapp.com/v4/access_token"
            token_data = {
                'app_id': ZALO_APP_ID,
                'app_secret': ZALO_APP_SECRET,
                'code': code
            }

            token_response = requests.post(token_url, data=token_data)
            token_json = token_response.json()

            if token_json.get('error'):
                api.abort(
                    400, f"Zalo OAuth error: {token_json.get('error_description')}")

            access_token = token_json.get('access_token')
            refresh_token = token_json.get('refresh_token')
            expires_in = token_json.get('expires_in', 3600)

            # Get user info from Zalo
            user_info_url = "https://graph.zalo.me/v2.0/me"
            headers = {'access_token': access_token}

            user_response = requests.get(user_info_url, headers=headers)
            user_json = user_response.json()

            if user_json.get('error'):
                api.abort(
                    400, f"Zalo API error: {user_json.get('error').get('message')}")

            zalo_id = user_json.get('id')
            zalo_name = user_json.get('name')
            zalo_avatar = user_json.get(
                'picture', {}).get('data', {}).get('url')

            # Tạo hoặc cập nhật user
            user_id = create_zalo_user(zalo_id, zalo_name, zalo_avatar,
                                       access_token, refresh_token, expires_in)

            if not user_id:
                api.abort(500, "Không thể tạo user từ Zalo")

            # Tạo session token
            session_token = create_session_token(user_id)
            user = get_user_by_id(user_id)

            # Clear OAuth state
            session.pop('oauth_state', None)

            return {
                'success': True,
                'message': 'Đăng nhập Zalo thành công',
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'avatar_url': user['avatar_url'],
                    'created_at': format_datetime_for_api(user['created_at'])
                },
                'session_token': session_token
            }, 200

        except Exception as e:
            logger.error(f"Zalo callback error: {e}")
            api.abort(500, f"Lỗi xử lý Zalo callback: {str(e)}")
