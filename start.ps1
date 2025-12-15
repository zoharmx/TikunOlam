# Tikun Olam - Quick Start Script (PowerShell)
# Starts both backend and frontend in development mode

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  תיקון עולם - Tikun Olam" -ForegroundColor Cyan
Write-Host "  Starting Development Environment" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ Error: .env file not found" -ForegroundColor Red
    Write-Host "Please create .env file with your API keys"
    exit 1
}

# Start backend
Write-Host "🚀 Starting backend API (port 8000)..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-Command", "uvicorn tikun.api.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if backend is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend failed to start" -ForegroundColor Red
    Write-Host "   Check the backend window for details"
    exit 1
}

# Start frontend
Write-Host "🎨 Starting frontend (port 3000)..." -ForegroundColor Green
Set-Location -Path "frontend"

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
}

# Start frontend in new window
Start-Process -FilePath "powershell" -ArgumentList "-Command", "npm run dev" -WindowStyle Normal

Set-Location -Path ".."

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  🎉 Tikun Olam is running!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "📍 API:       http://localhost:8000" -ForegroundColor White
Write-Host "📍 API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Close the PowerShell windows to stop the services" -ForegroundColor Yellow
Write-Host ""
