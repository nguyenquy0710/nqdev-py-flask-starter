import sys
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import requests

from app.config import Config, ENV_MODE

# Cấu hình thư mục logs trong BASE_DIR
# Dùng BASE_DIR hoặc mặc định là thư mục gốc
log_dir = os.path.join(Config.BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)  # Nếu thư mục logs không tồn tại, tạo mới

# Tạo đường dẫn file log
# Lấy ngày hiện tại và tạo tên file log theo ngày
# app-YYYY-MM-DD.log
log_file_name = f"app-{datetime.now().strftime('%Y-%m-%d')}.log"
log_file = os.path.join(log_dir, log_file_name)

# Cấu hình RotatingFileHandler để log không bị quá lớn (ví dụ: 10MB cho mỗi file)
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10 * 1024 * 1024,  # Kích thước tối đa 10MB
    backupCount=5,  # Giới hạn lưu tối đa 5 file log cũ
    encoding='utf-8'  # Đảm bảo file log sử dụng mã hóa UTF-8
)

# Cấu hình console handler với UTF-8 encoding
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))

# Đảm bảo console handler sử dụng mã hóa UTF-8
console_handler.encoding = 'utf-8'


# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        file_handler,       # Ghi log vào file app.log trong thư mục logs
        console_handler,    # Ghi log ra console
    ]
)


# Lấy logger toàn cục
logger = logging.getLogger(__name__)


class LoggingHelper:
    @staticmethod
    def log_requests_response(response: requests.Response, query: str = "", label: str = "SVR"):
        try:
            if response.status_code == 200:
                if response.text.strip():
                    print(f"[{label} ✅] Query thành công: {query.strip()}")
                    print(f"[{label} ✅] Response: {response.text.strip()}")
            else:
                print(f"[{label} ❌] Query thất bại: {query.strip()}")
                print(
                    f"[{label} ❌] Status: {response.status_code} - {response.reason}")
                print(f"[{label} ❌] Response: {response.text.strip()}")

        except Exception as e:
            print(f"[{label} ⚠️] Lỗi khi ghi log phản hồi: {e}")

    @staticmethod
    def get_logger():
        return logger

    @staticmethod
    def log_http_access(request_method, request_path, response_status):
        """Function to log HTTP access"""
        logger.info(
            f"[HTTP] {request_method} {request_path} - Status: {response_status}")
