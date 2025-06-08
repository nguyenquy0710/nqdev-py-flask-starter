import os
from flask import Flask
from flask_cors import CORS

from app.config import Config, logger
from app.web import web_bp
from app.api import api_bp
from app.db import init_app_db
from app.scheduler.jobs import start_scheduler


def create_app():
    """Factory function để tạo Flask application"""
    flask_env = os.getenv("FLASK_ENV", "production") or "development"
    logger.info(f"Khởi tạo ứng dụng trong môi trường: {flask_env}")

    flask_app = Flask(__name__)
    # flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

    # Cấu hình CORS cho API
    CORS(flask_app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

    # Load configuration
    flask_app.config.from_object(obj=Config)
    flask_app.secret_key = Config.SECRET_KEY

    # Khởi tạo DB
    try:
        init_app_db()
        logger.info("Database đã được khởi tạo thành công")
    except Exception as e:
        logger.error(f"Lỗi khởi tạo database: {e}")

    # Khởi tạo Scheduler
    try:
        start_scheduler()
        logger.info("Scheduler đã được khởi động thành công")
    except Exception as e:
        logger.error(f"Lỗi khởi động scheduler: {e}")

    # Import routes sau khi blueprint đã được tạo
    try:
        # Import routes cho web
        import app.web.common_routes
        import app.web.auth_routes

        # Import routes cho API
        import app.api.common_routes
        import app.api.auth_routes

        logger.info("Routes đã được import thành công")
    except Exception as e:
        logger.error(f"Lỗi import routes: {e}")

    # Đăng ký các Blueprint
    flask_app.register_blueprint(web_bp)
    flask_app.register_blueprint(api_bp)

    # Error handlers
    @flask_app.errorhandler(404)
    def not_found(error):
        return {"error": "Không tìm thấy tài nguyên"}, 404

    @flask_app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Lỗi server: {error}")
        return {"error": "Lỗi máy chủ nội bộ"}, 500

    @flask_app.errorhandler(400)
    def bad_request(error):
        return {"error": "Yêu cầu không hợp lệ"}, 400

    # Health check endpoint
    @flask_app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'message': 'Stock Tracker App đang hoạt động',
            'version': '1.0'
        }

    logger.info("Flask application đã được khởi tạo thành công")
    return flask_app
