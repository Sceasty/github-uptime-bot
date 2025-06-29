@echo off
chcp 65001 >nul
color 0a
setlocal enabledelayedexpansion

set TOKEN_DOSYA=token.token

if exist %TOKEN_DOSYA% (
    for /f "usebackq delims=" %%a in (%TOKEN_DOSYA%) do set TOKEN=%%a
) else (
    set TOKEN=
)

:ana_ekran
cls
echo.
echo       Uptime Bot
echo.
echo    [1- Start Bot]
echo    [2- Token Change]
echo.
set /p secim=Seciminizi giriniz (1 veya 2): 

if "!secim!"=="1" (
    echo Bot calistiriliyor...
    timeout /t 1 >nul
    python main.py
    echo.
    echo Bot kapandi. Enter'a basarak ana ekrana donun.
    pause >nul
    goto ana_ekran
) else if "!secim!"=="2" (
    call :token_degistir
    goto ana_ekran
) else (
    echo Yanlis secim! Tekrar deneyin.
    timeout /t 2 >nul
    goto ana_ekran
)

goto :eof

:token_degistir
cls
set /p yeni_token=Tokeni Giriniz: 
if "!yeni_token!"=="" (
    echo Token bos olamaz!
    echo Enter'e basarak ana ekrana donebilirsin!
    pause >nul
    goto ana_ekran
) else (
    echo !yeni_token!> %TOKEN_DOSYA%
    set TOKEN=!yeni_token!
    echo Token guncellendi.
    timeout /t 1 >nul
)
goto :eof
