@echo off
title Code2Video Builder

echo #############################################################
echo #                                                           #
echo #           Trinh xay dung ung dung Code2Video             #
echo #                                                           #
echo #############################################################
echo.
echo Chuan bi moi truong va cai dat cac goi phu thuoc...
echo Qua trinh nay co the mat vai phut tuy thuoc vao toc do mang.
echo Vui long khong tat cua so nay.
echo.

REM --- Kiem tra Python ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Khong tim thay Python.
    echo Vui long cai dat Python 3.8+ va dam bao no da duoc them vao PATH.
    pause
    exit /b 1
)

REM --- Tao moi truong ao ---
if not exist .venv (
    echo [*] Dang tao moi truong ao...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [LOI] Khong the tao moi truong ao.
        pause
        exit /b 1
    )
)

REM --- Kich hoat moi truong ao ---
call .venv\Scripts\activate

REM --- Cai dat cac goi phu thuoc ---
echo [*] Dang cai dat cac thu vien can thiet tu src/requirements.txt...
pip install --upgrade pip >nul
pip install -r src/requirements.txt
if %errorlevel% neq 0 (
    echo [LOI] Cai dat cac goi phu thuoc that bai.
    pause
    exit /b 1
)

echo [*] Dang cai dat PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo [LOI] Cai dat PyInstaller that bai.
    pause
    exit /b 1
)


REM --- Xay dung file .exe ---
echo.
echo #############################################################
echo #            Bat dau xay dung file Code2Video.exe           #
echo #############################################################
echo.
echo [*] Dang dong goi ung dung voi "sieu hook" va file cau hinh...
echo [*] Day la buoc ton nhieu thoi gian nhat.

REM --- Chay PyInstaller voi day du cac co de dam bao tinh on dinh ---
REM --- Loai bo add-data cho manim.cfg vi no duoc tao ra tu dong ---
pyinstaller --noconfirm ^
    --name Code2Video ^
    --add-data "assets;assets" ^
    --add-data "json_files;json_files" ^
    --add-data "prompts;prompts" ^
    --additional-hooks-dir ./hooks ^
    src/app.py

if %errorlevel% neq 0 (
    echo [LOI] Qua trinh dong goi that bai.
    pause
    exit /b 1
)

echo.
echo #############################################################
echo #                                                           #
echo #                  THANH CONG!                              #
echo #                                                           #
echo #############################################################
echo.
echo Ung dung da duoc xay dung thanh cong!
echo.
echo Ban co the tim thay ung dung trong thu muc:
echo %cd%\dist\Code2Video
echo.
echo De chay ung dung, hay vao thu muc tren va nhap dup vao file Code2Video.exe
echo.
pause
exit /b 0