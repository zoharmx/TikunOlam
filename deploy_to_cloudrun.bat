@echo off
echo ============================================================
echo  TIKUN OLAM - Deploy to Google Cloud Run
echo ============================================================
echo.
echo Project ID: tikunframework
echo Region: us-central1
echo Service: tikun-olam
echo.
echo This script will:
echo 1. Build Docker image using Cloud Build
echo 2. Deploy to Cloud Run
echo 3. Configure environment variables and secrets
echo.
echo Prerequisites:
echo - gcloud CLI installed and authenticated
echo - Project set to tikunframework
echo - Secrets created in Secret Manager (see DATADOG_SETUP_GUIDE.md)
echo.
pause

echo.
echo [1/4] Setting GCP project...
gcloud config set project tikunframework

echo.
echo [2/4] Building Docker image with Cloud Build...
echo This will take 5-10 minutes...
gcloud builds submit --config cloudbuild.yaml

echo.
echo [3/4] Deploying to Cloud Run...
echo Service will be available at: https://tikun-olam-xxxxxxxxxx-uc.a.run.app
gcloud run deploy tikun-olam ^
  --image gcr.io/tikunframework/tikun-olam:latest ^
  --region us-central1 ^
  --platform managed ^
  --allow-unauthenticated ^
  --memory 2Gi ^
  --cpu 2 ^
  --timeout 300s ^
  --concurrency 80 ^
  --min-instances 0 ^
  --max-instances 10 ^
  --set-env-vars "GCP_PROJECT_ID=tikunframework,GCP_LOCATION=us-central1,TIKUN_ENV=production,PYTHONUNBUFFERED=1" ^
  --set-secrets "GEMINI_API_KEY=GEMINI_API_KEY:latest,DEEPSEEK_API_KEY=DEEPSEEK_API_KEY:latest,DATADOG_API_KEY=DATADOG_API_KEY:latest,DATADOG_APP_KEY=DATADOG_APP_KEY:latest"

echo.
echo [4/4] Getting service URL...
gcloud run services describe tikun-olam --region us-central1 --format "value(status.url)"

echo.
echo ============================================================
echo  Deployment Complete!
echo ============================================================
echo.
echo Test your deployment:
echo 1. Open the URL shown above
echo 2. Add /docs to see the API documentation
echo 3. Try the /health endpoint
echo.
echo Example:
echo   curl https://your-service-url/health
echo.
pause
