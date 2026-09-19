# AEROFARM Launch Script (Windows)

Write-Host "🚀 Launching AEROFARM..." -ForegroundColor Cyan

# Start Backend
Write-Host "📦 Starting Backend (FastAPI)..." -ForegroundColor Green
Start-Process powershell -NoNewWindow -ArgumentList "python -m backend.app"

# Start Frontend
Write-Host "🌐 Starting Frontend (Vite)..." -ForegroundColor Blue
Set-Location frontend
npm run dev

# Keep window open if the dev server stops
Read-Host "Press Enter to exit"
