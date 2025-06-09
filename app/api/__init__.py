from flask import Blueprint
from flask_restx import Api, Resource, fields

from app.config import ENV_MODE

api_bp = Blueprint("api", __name__)  # , url_prefix="/api")

# Khởi tạo Flask-RESTX API với Swagger
api = Api(
    api_bp,
    version='1.0',
    title='Stock Tracker API',
    description='API để theo dõi và phân tích giá cổ phiếu Việt Nam',
    # Swagger UI sẽ có tại /api/swagger/
    doc=None if ENV_MODE == 'prod' else '/swagger/',
    prefix='/api'
)


# Định nghĩa các model cho Swagger documentation
api_error_model = api.model('Error', {
    'error': fields.String(required=True, description='Mô tả lỗi'),
    'code': fields.Integer(description='Mã lỗi')
})
