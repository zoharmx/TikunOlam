@echo off
echo ============================================================
echo  TIKUN OLAM - Installing Updated Dependencies
echo ============================================================
echo.

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installing backend dependencies (Vertex AI + Datadog)...
pip install -r requirements.txt

echo.
echo [3/3] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Run test: python test_vertex_migration.py
echo 2. Start backend: uvicorn src.tikun.api.main:app --reload
echo 3. Start frontend: cd frontend ^&^& npm run dev
echo.
pause
