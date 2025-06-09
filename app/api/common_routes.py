from flask import jsonify, request
from flask_restx import Api, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from . import api_bp, api, api_error_model
from app.config import Config
from app.db.sqlite_handler import get_all_symbols

# Định nghĩa các model cho Swagger documentation
common_symbol_model = api.model('Symbol', {
    'id': fields.Integer(required=True, description='ID của symbol'),
    'symbol': fields.String(required=True, description='Mã cổ phiếu (VD: VIC, VCB)'),
    'name': fields.String(description='Tên công ty'),
    'created_at': fields.DateTime(description='Thời gian thêm vào hệ thống')
})


# Namespace cho việc tổ chức API
ns_common = api.namespace(
    'symbols', description='Quản lý danh sách mã cổ phiếu')


@ns_common.route('')
class SymbolsList(Resource):
    @ns_common.doc('list_symbols')
    @ns_common.marshal_list_with(common_symbol_model)
    @ns_common.response(200, 'Thành công')
    @ns_common.response(500, 'Lỗi server', api_error_model)
    def get(self):
        """Lấy danh sách tất cả mã cổ phiếu đang theo dõi"""
        try:
            symbols = get_all_symbols()
            return symbols, 200
        except Exception as e:
            api.abort(500, f"Lỗi khi lấy danh sách symbols: {str(e)}")


# Health check endpoint
@ns_common.route('/health')
class HealthCheck(Resource):
    @ns_common.doc('health_check')
    @ns_common.response(200, 'API đang hoạt động')
    def get(self):
        """Kiểm tra trạng thái hoạt động của API"""
        return {
            'status': 'healthy',
            'message': 'Stock Tracker API đang hoạt động bình thường',
            'version': '1.0'
        }, 200
