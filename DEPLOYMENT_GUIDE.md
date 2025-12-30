# Tikun Olam - Complete Deployment Guide

**From Local Development to Production on Google Cloud Run**

---

## Deployment Options

### Option A: Local Demo (Recommended for Hackathon)
- ✅ Fastest setup (no deployment needed)
- ✅ Perfect for video demo
- ✅ No additional GCP costs
- ⚠️ Only accessible on your machine

**Use this if:** You're short on time and just need a working demo for the video.

### Option B: Cloud Run Deployment (Impressive but Optional)
- ✅ Publicly accessible URL
- ✅ Production-ready infrastructure
- ✅ Auto-scaling
- ✅ More impressive for judges
- ⚠️ Requires additional setup
- ⚠️ Small GCP costs (~$0.50-2.00 for hackathon period)

**Use this if:** You have time and want to show a live deployment in your submission.

---

## Option A: Local Demo Setup (30 minutes)

### Step 1: Configure Datadog (RECOMMENDED)
Follow the complete guide: **DATADOG_SETUP_GUIDE.md**

Quick version:
```powershell
# 1. Create Datadog account (free trial): https://www.datadoghq.com/
# 2. Get API keys from Organization Settings
# 3. Add to .env:
DATADOG_API_KEY=your-api-key
DATADOG_APP_KEY=your-app-key

# 4. Upload dashboard
python monitoring/upload_dashboard.py

# 5. Create monitors
python monitoring/create_monitors.py
```

### Step 2: Start Backend
```powershell
# From TikunOlam root directory
uvicorn src.tikun.api.main:app --reload --port 8000
```

**Verify:**
- Open: http://localhost:8000/health
- Should return: `{"status": "healthy"}`
- Check logs for: `Datadog initialized successfully`

### Step 3: Start Frontend
```powershell
# In new terminal
cd frontend
npm run dev
```

**Verify:**
- Open: http://localhost:5173
- Should show Tikun Olam dashboard
- No errors in browser console

### Step 4: Test Full Pipeline
1. Enter scenario:
   ```
   A city council is considering implementing a universal basic income (UBI)
   program funded by a 2% tax on automated services. The program would provide
   $1000/month to all residents earning less than $50,000/year.
   ```
2. Click "Analyze Scenario"
3. Wait ~30-60 seconds
4. View results in "Results" tab
5. Check "Observability" tab for metrics
6. Check Datadog dashboard for data (wait 2-3 minutes)

### Step 5: Record Video
- Follow **VIDEO_DEMO_SCRIPT.md** for detailed instructions
- Show: Frontend → Analysis → Observability Panel → Datadog Dashboard
- Emphasize BinahSigma bias_delta metric

**You're done!** This is sufficient for a winning submission.

---

## Option B: Cloud Run Deployment (2-3 hours)

### Prerequisites Checklist
- [x] GCP project: algebraic-craft-453221-g1
- [ ] gcloud CLI installed and authenticated
- [ ] Datadog configured (see DATADOG_SETUP_GUIDE.md)
- [ ] Docker installed locally (for testing)
- [ ] Secrets created in Secret Manager

### Step 1: Create Secrets in Google Cloud Secret Manager

**Required Secrets:**
1. GEMINI_API_KEY
2. DEEPSEEK_API_KEY
3. DATADOG_API_KEY
4. DATADOG_APP_KEY

**Create them:**
```powershell
# Set project
gcloud config set project algebraic-craft-453221-g1

# Create GEMINI_API_KEY secret
echo "YOUR_GEMINI_KEY" | gcloud secrets create GEMINI_API_KEY --data-file=-

# Create DEEPSEEK_API_KEY secret
echo "YOUR_DEEPSEEK_KEY" | gcloud secrets create DEEPSEEK_API_KEY --data-file=-

# Create DATADOG_API_KEY secret
echo "YOUR_DATADOG_API_KEY" | gcloud secrets create DATADOG_API_KEY --data-file=-

# Create DATADOG_APP_KEY secret
echo "YOUR_DATADOG_APP_KEY" | gcloud secrets create DATADOG_APP_KEY --data-file=-

# Grant Cloud Run access to secrets
$PROJECT_NUMBER = (gcloud projects describe algebraic-craft-453221-g1 --format="value(projectNumber)")
$SERVICE_ACCOUNT = "$PROJECT_NUMBER-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding GEMINI_API_KEY --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding DEEPSEEK_API_KEY --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding DATADOG_API_KEY --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding DATADOG_APP_KEY --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
```

**Verify secrets:**
```powershell
gcloud secrets list
```

Should show all 4 secrets.

### Step 2: Enable Required APIs
```powershell
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### Step 3: Test Docker Build Locally (Optional but Recommended)
```powershell
# Build image
docker build -t tikun-olam:test .

# This will take 5-10 minutes (multi-stage build)
```

**If build fails:**
- Check Docker is running
- Verify `frontend/package.json` exists
- Check `requirements.txt` is valid
- See troubleshooting section below

### Step 4: Deploy Using Automated Script

**Windows:**
```powershell
.\deploy_to_cloudrun.bat
```

**Mac/Linux:**
```bash
chmod +x deploy_to_cloudrun.sh
./deploy_to_cloudrun.sh
```

**What it does:**
1. Sets GCP project to algebraic-craft-453221-g1
2. Builds Docker image using Cloud Build (~5-10 min)
3. Deploys to Cloud Run with all configurations
4. Returns public URL

**Expected duration:** 10-15 minutes

### Step 5: Get Service URL
After deployment completes:
```powershell
gcloud run services describe tikun-olam --region us-central1 --format "value(status.url)"
```

**Example output:**
```
https://tikun-olam-abc123-uc.a.run.app
```

**Save this URL!** You'll use it in:
- Devpost submission
- Video demo
- Testing

### Step 6: Test Deployment

**Health check:**
```powershell
curl https://YOUR-SERVICE-URL/health
```

**API docs:**
```
https://YOUR-SERVICE-URL/docs
```

**Test analysis:**
```powershell
curl -X POST https://YOUR-SERVICE-URL/analyze `
  -H "Content-Type: application/json" `
  -d '{\"scenario\": \"Test scenario\", \"case_name\": \"test\"}'
```

### Step 7: Configure Frontend for Production (Optional)

If you want to deploy frontend separately to Firebase Hosting:

**1. Update frontend/.env.production:**
```bash
VITE_API_URL=https://YOUR-CLOUD-RUN-URL
VITE_DATADOG_APP_ID=your-rum-app-id
VITE_DATADOG_CLIENT_TOKEN=your-rum-token
VITE_DATADOG_SITE=datadoghq.com
```

**2. Build frontend:**
```powershell
cd frontend
npm run build
```

**3. Deploy to Firebase Hosting:**
```powershell
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize (if not done)
firebase init hosting

# Deploy
firebase deploy --only hosting
```

---

## Cloud Build CI/CD (Advanced)

The `cloudbuild.yaml` file provides automated deployment on every git push.

### Setup Continuous Deployment:

**1. Connect GitHub repository:**
```powershell
# Go to Cloud Build in GCP Console
https://console.cloud.google.com/cloud-build/triggers

# Click "Create Trigger"
# Connect your GitHub repository
# Select branch: main
# Build configuration: cloudbuild.yaml
# Click "Create"
```

**2. Push to trigger deployment:**
```powershell
git add .
git commit -m "Deploy to Cloud Run"
git push origin main
```

**3. Monitor build:**
```powershell
gcloud builds list --limit=5
```

Or view in console:
```
https://console.cloud.google.com/cloud-build/builds
```

---

## Cost Estimation

### Cloud Run Costs (for hackathon period):
- **Build time:** ~10 min × $0.003/min = $0.03
- **Container image storage:** ~500 MB × $0.026/GB = $0.01
- **Request execution:** 100 requests × 30s avg × $0.00002/sec = $0.06
- **Memory:** 2GB × 100 requests × 30s × $0.0000025/GB-sec = $0.015

**Total estimated: $0.12 - $0.50 for entire hackathon**

### Free tier includes:
- 2 million requests/month
- 360,000 GB-seconds/month
- 180,000 vCPU-seconds/month

**You'll likely stay within free tier for the hackathon!**

### To minimize costs:
- Set `--min-instances 0` (already configured)
- Delete service after submission if not needed:
  ```powershell
  gcloud run services delete tikun-olam --region us-central1
  ```

---

## Troubleshooting

### Issue: Docker build fails with "COPY failed"
**Solution:**
- Make sure you're running docker build from TikunOlam root directory
- Check that all files in Dockerfile COPY commands exist
- Verify `.dockerignore` isn't excluding required files

### Issue: Cloud Build fails with "permission denied"
**Solution:**
```powershell
# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Grant Cloud Build service account permissions
$PROJECT_NUMBER = (gcloud projects describe algebraic-craft-453221-g1 --format="value(projectNumber)")
gcloud projects add-iam-policy-binding algebraic-craft-453221-g1 `
  --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" `
  --role="roles/run.admin"
```

### Issue: Deployment succeeds but service crashes
**Solution:**
```powershell
# Check logs
gcloud run services logs read tikun-olam --region us-central1

# Common issues:
# 1. Missing secrets - verify secrets exist and permissions are granted
# 2. PORT environment variable - Cloud Run sets this automatically
# 3. Health check failing - verify /health endpoint works
```

### Issue: "Secret not found" error
**Solution:**
```powershell
# List secrets
gcloud secrets list

# Verify secret has data
gcloud secrets versions access latest --secret="GEMINI_API_KEY"

# Re-create if needed
gcloud secrets delete GEMINI_API_KEY
echo "YOUR_KEY" | gcloud secrets create GEMINI_API_KEY --data-file=-
```

### Issue: Frontend can't connect to backend
**Solution:**
- Check CORS settings in `src/tikun/api/main.py`
- Verify frontend has correct API URL
- Check browser console for CORS errors
- Ensure Cloud Run allows unauthenticated requests (or add auth)

### Issue: Datadog metrics not appearing
**Solution:**
- Verify secrets are correctly set in Cloud Run
- Check Cloud Run logs for "Datadog initialized successfully"
- Wait 5-10 minutes for metrics to appear
- Verify API keys are correct in Secret Manager

---

## Monitoring Production Deployment

### View Logs:
```powershell
# Real-time logs
gcloud run services logs tail tikun-olam --region us-central1

# Recent logs
gcloud run services logs read tikun-olam --region us-central1 --limit 50
```

### View Metrics (GCP):
```
https://console.cloud.google.com/run/detail/us-central1/tikun-olam/metrics
```

### View Metrics (Datadog):
- Go to your Datadog dashboard URL (from DATADOG_SETUP_GUIDE.md)
- Should see production metrics tagged with `env:production`

### Set up Alerts:
Cloud Run alerts are already configured in `monitoring/create_monitors.py`.

Additional GCP alerts:
```powershell
# Alert on high error rate
gcloud alpha monitoring policies create --notification-channels=CHANNEL_ID \
  --display-name="Tikun Olam Error Rate" \
  --condition-display-name="Error rate > 5%" \
  ...
```

---

## Deployment Checklist

### Before Deployment:
- [ ] All tests pass: `python test_vertex_migration.py`
- [ ] Backend runs locally without errors
- [ ] Frontend builds successfully: `cd frontend && npm run build`
- [ ] Datadog configured and dashboard uploaded
- [ ] Secrets created in Secret Manager
- [ ] Required APIs enabled

### During Deployment:
- [ ] Cloud Build completes successfully
- [ ] Image pushed to Container Registry
- [ ] Cloud Run service deployed
- [ ] Health check returns 200 OK
- [ ] No errors in Cloud Run logs

### After Deployment:
- [ ] Service URL accessible
- [ ] /health endpoint returns healthy
- [ ] /docs shows API documentation
- [ ] Can submit analysis via API
- [ ] Metrics appear in Datadog (wait 5-10 min)
- [ ] URL added to Devpost submission
- [ ] URL tested in video demo

---

## Production Best Practices (Optional)

If you continue using this after the hackathon:

### Security:
```powershell
# 1. Require authentication
gcloud run services update tikun-olam --no-allow-unauthenticated

# 2. Use custom domain with HTTPS
gcloud run domain-mappings create --service tikun-olam --domain yourdomain.com

# 3. Set up VPC connector for private services
```

### Scaling:
```powershell
# Increase max instances for high traffic
gcloud run services update tikun-olam --max-instances 100

# Set min instances to reduce cold starts (costs $$$)
gcloud run services update tikun-olam --min-instances 1
```

### Monitoring:
```powershell
# Set up error reporting
gcloud services enable clouderrorreporting.googleapis.com

# Set up uptime checks
# Configure in: https://console.cloud.google.com/monitoring/uptime
```

---

## Rollback (If Something Goes Wrong)

### Rollback to previous revision:
```powershell
# List revisions
gcloud run revisions list --service tikun-olam --region us-central1

# Rollback to specific revision
gcloud run services update-traffic tikun-olam \
  --to-revisions REVISION-NAME=100 \
  --region us-central1
```

### Delete deployment:
```powershell
# Delete Cloud Run service
gcloud run services delete tikun-olam --region us-central1

# Delete container images
gcloud container images delete gcr.io/algebraic-craft-453221-g1/tikun-olam:latest
```

---

## For Hackathon Submission

### What to include in Devpost:

**If Local Demo (Option A):**
- ✅ "Demo available locally (see video)"
- ✅ GitHub repository with full code
- ✅ Setup instructions in README.md
- ✅ Video showing working system

**If Deployed (Option B):**
- ✅ Live demo URL: https://your-cloud-run-url
- ✅ API documentation: https://your-cloud-run-url/docs
- ✅ GitHub repository
- ✅ Video showing deployed system

**Both options are equally valid for the hackathon!**

---

## Summary

### Recommended Path:
1. ✅ **Start with local demo** (Option A) - fastest, zero risk
2. ✅ **Configure Datadog** - required for challenge, high impact
3. ✅ **Record video** with local demo
4. ⏳ **Deploy to Cloud Run** (Option B) - only if you have extra time

### Time Investment:
- **Local Demo:** 30-60 minutes
- **Cloud Run Deployment:** 2-3 hours additional
- **Datadog Configuration:** 30-45 minutes (highly recommended)

### Priority:
1. **CRITICAL:** Working local demo with Datadog
2. **CRITICAL:** Video showing BinahSigma + observability
3. **HIGH:** Devpost submission with all required info
4. **MEDIUM:** Cloud Run deployment (nice to have)

---

**You're fully equipped to deploy Tikun Olam!** 🚀

Choose the path that best fits your timeline. Remember: **A great video with a local demo is better than a mediocre video with Cloud Run deployment.**

**Focus on showcasing BinahSigma and Datadog observability - that's what will win the hackathon!**

---

**Created:** December 24, 2025
**Next Steps:** Follow DATADOG_SETUP_GUIDE.md → Record video → Submit!
