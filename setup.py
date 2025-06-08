from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Đọc version từ .version.txt (được tạo trong CI)
try:
    with open(".version.txt") as f:
        version = f.read().strip()
except FileNotFoundError:
    version = "0.0.0"  # fallback nếu chạy local

# Đọc dependencies từ requirements.txt
try:
    with open("requirements.txt", "r") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]
except FileNotFoundError:
    requirements = []

setup(
    name="stock-tracker-app",         # ⚠️ Đặt đúng tên ứng dụng/module
    version=version,
    description="Stock tracking app using Flask",
    install_requires=requirements,
    author="Nguyen Quy",
    author_email="quy.nh@nhquydev.net",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",          # Có thể chỉnh tùy app của bạn
)
