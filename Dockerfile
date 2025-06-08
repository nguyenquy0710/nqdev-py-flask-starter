# Sử dụng image base là Python slim
FROM python:3.10-slim

LABEL org.opencontainers.image.description="Stock tracking app using Flask"

USER root

# Đặt biến môi trường để Python không tạo file .pyc và in log ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy requirements.txt vào thư mục /app trong container
COPY requirements.txt /app/

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ nội dung dự án vào thư mục /app trong container
COPY . /app/

# Mở cổng ứng dụng (ví dụ: 5000 nếu chạy với waitress hoặc Flask)
EXPOSE 5000

# Lệnh chạy chính khi container khởi động
CMD ["python", "start_waitress.py"]
