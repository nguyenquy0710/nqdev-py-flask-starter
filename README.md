# 🧱 nqdev-py-flask-starter

A simple and clean **Python Flask project template** with pre-defined structure and common modules. Ideal for quickly starting new Flask-based RESTful APIs or small web applications.

---

## 🚀 Features

- 📁 Predefined project structure
- ♻️ Common utilities (logging, configs, error handling, etc.)
- 🧪 Ready for development and extension
- 🐳 Optional Docker support (add if needed)
- 📦 Easy to scale and maintain

---

## 📂 Project Structure

```bash
nqdev-py-flask-starter/
├── app.py                         # App chính để chạy (tích hợp API & Web UI)
├── config.py                      # Cấu hình (host, port, key...)
├── requirements.txt               # Thư viện cần cài
│
├── config/
│   ├── __init__.py
│   ├── config_dev.py              # ✅ Dành cho local development
│   ├── config_prod.py             # ✅ Dành cho production (VD: máy chủ thật)
│   └── config_test.py             # ✅ Dành cho unit test (dùng in-memory DB)
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
└── tests/
│   └── test_questdb_service.py
│
│
```

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/nqdev-py-flask-starter.git
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

## 📄 License

[MIT](LICENSE) – feel free to use, modify, and distribute.

