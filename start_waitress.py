import os
from waitress import serve as run_serve

from app import create_app

appFlask = create_app()

__FLASK_ENV__: str = os.getenv("FLASK_ENV", "production").lower()

# Start the server using Waitress
if __name__ == '__main__':
    # Kiểm tra môi trường Flask (production hay development)
    if __FLASK_ENV__ == 'production':
        # Sự kiện log thông tin khi khởi động server
        # on_start(flask_env=__FLASK_ENV__)

        # Log thông tin về việc khởi động server trong môi trường sản xuất
        # logger.info(f"Starting server with Waitress on http://localhost:5000")
        print(f'ApiDocs on http://localhost:5000/swagger/')

        # Sử dụng Waitress để chạy Flask ứng dụng
        # '0.0.0.0' để có thể truy cập từ bên ngoài
        run_serve(app=appFlask, host='0.0.0.0', port=5000)
    else:
        # Nếu là môi trường phát triển (development), sử dụng Flask tự động
        # on_start(flask_env=__FLASK_ENV__)

        # Log thông tin về việc khởi động server trong môi trường phát triển
        # logger.info("Running Flask in development mode with flask.run()")

        # Chạy ứng dụng Flask trong môi trường phát triển
        appFlask.run(host='localhost', port=5000, debug=True)

# Python WSGI server
# https://flask.palletsprojects.com/en/stable/deploying/waitress/
