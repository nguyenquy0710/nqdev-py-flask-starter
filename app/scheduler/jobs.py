from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

# Import các module để truy vấn dữ liệu và gửi tới QuestDB
from app.config import Config  # Nhập logger từ config
from app.helpers.logging_helper import logger


def auto_update():
    """
    Hàm này sẽ lấy danh sách các symbols từ cơ sở dữ liệu,
    sau đó lấy giá của từng symbol từ Vietstock và gửi đến QuestDB.
    """
    logger.info("Bat dau chay auto_update...")  # Log thông tin khi job bắt đầu


def start_scheduler():
    """
    Hàm này sẽ khởi tạo một BackgroundScheduler và thêm một job auto_update
    chạy mỗi phút trong khoảng từ 9h sáng đến 5h chiều (9:00-17:00).
    """
    # Lấy giá trị của biến môi trường ENABLE_AUTO_UPDATE
    enable_auto_update = Config.ENABLE_AUTO_UPDATE

    if enable_auto_update:
        scheduler = BackgroundScheduler()

        # Sử dụng CronTrigger để lên lịch auto_update mỗi ngày từ 9h sáng tới 5h chiều
        # Chạy mỗi phút trong khoảng 9h-17h, mỗi giờ từ 9 đến 17 và mỗi phút từ 0 đến 59
        minutely_trigger_during_working_hours = CronTrigger(
            hour='9-17', minute='0-59', second='0')
        auto_update_half_hour_trigger = CronTrigger(
            hour='9-17', minute='0,30', second='0')

        # Thêm job vào scheduler
        scheduler.add_job(auto_update, auto_update_half_hour_trigger)

        # Bắt đầu scheduler trong background
        scheduler.start()
        logger.info(
            "Scheduler đã bắt đầu và sẽ tự động cập nhật mỗi phút trong khoảng giờ làm việc (9h-17h).")
    else:
        logger.info(
            "Scheduler bị tắt do biến môi trường ENABLE_AUTO_UPDATE không được thiết lập.")
