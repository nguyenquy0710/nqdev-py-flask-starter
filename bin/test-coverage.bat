@echo off
setlocal ENABLEDELAYEDEXPANSION

echo [🧪] Dang chay test voi coverage...

call cls
@REM call cd ../

REM ✅ Set môi trường test
set APP_ENV=test

REM ✅ Kích hoạt virtualenv nếu cần
call env\Scripts\activate

REM ✅ Xóa thư mục htmlcov cũ nếu tồn tại
if exist htmlcov (
    echo [🧹] Xoa thu muc htmlcov cu...
    rmdir /s /q htmlcov
)

REM ✅ Chạy pytest + coverage
coverage run -m pytest

REM ✅ In báo cáo ra console
coverage report

REM ✅ Tạo báo cáo HTML (xem đẹp hơn)
coverage html

REM ✅ Mở báo cáo HTML bằng trình duyệt mặc định
echo.
echo [🌐] Mo bao cao HTML: htmlcov\index.html
start "" htmlcov\index.html