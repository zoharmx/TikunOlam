@echo off
echo ========================================
echo Tikun Olam - Graphics Generator
echo ========================================
echo.

echo Verificando instalacion de matplotlib...
python -c "import matplotlib" 2>nul
if errorlevel 1 (
    echo matplotlib no esta instalado. Instalando...
    pip install matplotlib
) else (
    echo matplotlib OK
)

echo.
echo Creando carpeta de graficos...
mkdir images\graphics 2>nul

echo.
echo ========================================
echo Generando graficos...
echo ========================================

echo.
echo [1/2] Generando Divergence Meter 75%%...
python create_divergence_meter.py

echo.
echo [2/2] Generando Decision Flow Diagram...
python create_decision_flow.py

echo.
echo ========================================
echo Completado!
echo ========================================
echo.
echo Graficos guardados en: images\graphics\
echo.
pause
