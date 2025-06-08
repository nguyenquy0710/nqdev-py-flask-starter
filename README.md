[![Python CI/CD with Flask and Docker](https://github.com/nguyenquy0710/nqdev-py-flask-starter/actions/workflows/py-flask-ci-cd.yml/badge.svg)](https://github.com/nguyenquy0710/nqdev-py-flask-starter/actions/workflows/py-flask-ci-cd.yml)
[![Update Changelog on Release](https://github.com/nguyenquy0710/nqdev-py-flask-starter/actions/workflows/changelog.yml/badge.svg)](https://github.com/nguyenquy0710/nqdev-py-flask-starter/actions/workflows/changelog.yml)

# 🧱 nqdev-py-flask-starter

A simple and clean **Python Flask project template** with pre-defined structure and common modules. Ideal for quickly starting new Flask-based RESTful APIs or small web applications.

---

## 🚀 Features

- 📁 Predefined project structure
- ♻️ Common utilities (logging, configs, error handling, etc.)
- ⚙️ Easy to extend and maintain
- 🧪 Ready for development and extension
- 🐳 Optional Docker support (add if needed)
- 📦 Easy to scale and maintain
- 📄 Includes [CHANGELOG.md](./CHANGELOG.md) to track project updates

---

## 📂 Project Structure

```bash
stock_app/
├── app/                           # 📦 Thư mục chính chứa mã nguồn
│   ├── __init__.py                # Biến app thành package Python, chứa create_app()
│   │
│   ├── web/                       # ✅ module web_bp
│   │
│   ├── api/                       # ✅ module api_bp
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config_dev.py          # ✅ Dành cho local development
│   │   ├── config_prod.py         # ✅ Dành cho production (VD: máy chủ thật)
│   │   └── config_test.py         # ✅ Dành cho unit test (dùng in-memory DB)
│
├── app.py                         # ✅ để chạy local
├── config.py                      # Cấu hình (host, port, key...)
├── requirements.txt               # Thư viện cần cài
├── setup.py                       # ⚙️ Cấu hình build (đã chuẩn hoá)
├── .version.txt                   # 🔖 Ghi từ CI/CD (không cần commit)
├── VERSION                        # Base version (ví dụ: "1.0")
├── Dockerfile
├── README.md
├── pyproject.toml                 # Tuỳ chọn (nếu dùng setuptools hiện đại)
│

│
├── api/                           # Flask blueprint cho API (JSON)
│   ├── __init__.py                # Tạo Blueprint api_bp
│   └── routes.py                  # Các route RESTful
│
├── web/                           # Flask blueprint cho Web UI (giao diện người dùng)
│   ├── __init__.py                # Tạo Blueprint web_bp
│   └── routes.py                  # Các route hiển thị HTML
│
├── db/
│   ├── __init__.py
│   ├── sqlite_handler.py          # Xử lý SQLite: add, get, delete symbols
│   └── questdb_client.py          # Gửi dữ liệu qua TCP tới QuestDB
│
├── data/
│   └── symbols.db                 # Sqlite Database Path
│
├── analytics/
│   └── indicators.py              # Tính toán chỉ báo kỹ thuật
│
├── services/
│   ├── __init__.py
│   └── vietstock.py               # Gọi API lấy giá từ Vietstock
│
└── scheduler/
│   └── jobs.py                    # Hàm cập nhật giá tự động theo lịch
│
├── templates/
│   └── index.html                 # Giao diện HTML
│
├── static/                        # (tuỳ chọn) CSS/JS tĩnh
│
├── tests/                         # ✅ Unit tests
│   ├── __init__.py
│   └── test_questdb_service.py
│
│

```

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/nguyenquy0710/nqdev-py-flask-starter.git
cd nqdev-py-flask-starter
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Run the app

```bash
python run.py
```

By default, the app runs on http://127.0.0.1:5000

## 🧩 Customize

Start adding your routes in `app/routes/`, business logic in `services/`, and shared code in `common/`. Configuration can be adjusted via `config/config.py`.

## 📌 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the list of updates, versions, and improvements.

## 📄 License

[MIT](LICENSE) – feel free to use, modify, and distribute.
