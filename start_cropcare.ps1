# CropCare AI PowerShell Launcher
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "       Starting CropCare AI Platform (Full-Stack)            " -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green

$RootPath = $PSScriptRoot
if (-not $RootPath) { $RootPath = Get-Location }

# 1. Start Backend
Write-Host "[1/2] Launching Backend on http://127.0.0.1:8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\backend'; .\venv\Scripts\activate; python run_backend.py"

# 2. Start Frontend
Write-Host "[2/2] Launching Frontend on http://localhost:5173..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PATH = 'C:\Program Files\nodejs;' + `$env:PATH; cd '$RootPath\frontend'; npm run dev"

Start-Sleep -Seconds 3

# 3. Open Browser
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

Write-Host "`nCropCare AI is now running!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "API Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
