import sys
import os

# Agrega la carpeta src al path de Python para poder importar tikun
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from tikun.api.main import app

# Vercel serverless function entrypoint
# No es necesario ejecutar uvicorn aquí, Vercel maneja el ciclo de vida