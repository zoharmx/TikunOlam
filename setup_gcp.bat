@echo off
echo ============================================================
echo  TIKUN OLAM - GCP Vertex AI Setup
echo ============================================================
echo.
echo Project ID: algebraic-craft-453221-g1
echo Location: us-central1
echo.
echo This script will:
echo 1. Set your GCP project
echo 2. Enable Vertex AI API
echo 3. Configure application credentials
echo.
echo Prerequisites:
echo - gcloud CLI installed (https://cloud.google.com/sdk/docs/install)
echo - Logged in to gcloud (gcloud auth login)
echo.
pause

echo.
echo [1/3] Setting GCP project...
gcloud config set project algebraic-craft-453221-g1

echo.
echo [2/3] Enabling Vertex AI API...
gcloud services enable aiplatform.googleapis.com

echo.
echo [3/3] Configuring application default credentials...
echo This will open a browser window for authentication...
gcloud auth application-default login

echo.
echo ============================================================
echo  GCP Setup Complete!
echo ============================================================
echo.
echo You can now run: python test_vertex_migration.py
echo.
pause
