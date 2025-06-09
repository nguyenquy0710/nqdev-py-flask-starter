import os
from dotenv import load_dotenv

# ✅ Load .env nếu tồn tại
load_dotenv()

# Ưu tiên lấy từ biến môi trường, mặc định là "dev"
ENV_MODE = os.getenv("APP_ENV", "dev")

if ENV_MODE == "prod":
    from .config_prod import Config
elif ENV_MODE == "test":
    from .config_test import Config
else:
    from .config_dev import Config
