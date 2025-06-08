### 📁 Cấu trúc thư mục chuẩn hoá:

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

### 🧠 Phân tích vai trò từng phần:

| Tệp / Thư mục             | Vai trò                                                     |
| ------------------------- | ----------------------------------------------------------- |
| `app.py`                  | Flask entrypoint, định tuyến và render                      |
| `config/*.py`             | Các hằng số cấu hình (host, port, secret_key...)            |
| `db/sqlite_handler.py`    | Hàm SQLite: init_db(), add_symbol(), get_all_symbols()...   |
| `db/questdb_client.py`    | Hàm gửi dữ liệu tới QuestDB bằng TCP (Influx Line Protocol) |
| `services/vietstock.py`   | Hàm get_price_vietstock(symbol) và is_valid_symbol(symbol)  |
| `scheduler/jobs.py`       | Hàm auto_update() + tích hợp APScheduler                    |
| `analytics/indicators.py` | Tính toán RSI, SMA, EMA, Bollinger Bands...                 |

### ✅ 4. Cách chuyển môi trường

#### 🧪 Mặc định (dev):

```bash
python app.py
```

#### 🌐 Dùng production:

```bash
set APP_ENV=prod && python app.py
```

#### 🧪 Dùng trong test:

```bash
set APP_ENV=test && pytest
```
