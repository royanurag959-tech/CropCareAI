@echo off
title CropCare AI Launcher
echo ==============================================================
echo       Starting CropCare AI Platform (Full-Stack)
echo ==============================================================

cd /d "%~dp0"

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "CropCare Backend API" cmd /k "cd backend && venv\Scripts\activate && python run_backend.py"

echo [2/2] Starting Vite Frontend on http://localhost:5173 ...
set "PATH=C:\Program Files\nodejs;%PATH%"
start "CropCare Frontend" cmd /k "cd frontend && npm run dev"

echo Waiting for servers to initialize...
timeout /t 3 >nul

echo Opening CropCare AI in your browser...
start http://localhost:5173

echo ==============================================================
echo   CropCare AI is now LIVE!
echo   - Web App: http://localhost:5173
echo   - Backend Swagger Docs: http://127.0.0.1:8000/docs
echo ==============================================================
