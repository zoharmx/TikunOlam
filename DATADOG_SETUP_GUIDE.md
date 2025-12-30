# Datadog Configuration Guide - Tikun Olam

**Complete step-by-step guide to enable full observability for the hackathon demo**

---

## Why Configure Datadog?

Datadog integration is **REQUIRED** for the Google Cloud AI Partner Catalyst - Datadog Challenge. Without it, you won't be able to:
- ❌ Show the observability dashboard in your video
- ❌ Demonstrate BinahSigma bias_delta metrics
- ❌ Display real-time alerts on ethical violations
- ❌ Fully meet the challenge requirements

**Time Required:** 30-45 minutes
**Cost:** FREE (14-day trial, no credit card required)
**Value:** +40% win probability for hackathon

---

## Step 1: Create Datadog Account (5 minutes)

### 1.1 Sign Up
1. Go to: https://www.datadoghq.com/
2. Click **"Get Started Free"** or **"Try Datadog Free"**
3. Fill out the form:
   - **Email:** Your email address
   - **Company:** "Tikun Olam Project" or your name
   - **Country:** United States
   - **Number of hosts:** Select "1-10"
4. Click **"Create Account"**
5. Check your email for verification link
6. Click verification link to activate account

### 1.2 Choose Region
- **Recommended:** US5 (us5.datadoghq.com)
- **Alternative:** US1 (app.datadoghq.com)

**Important:** Remember which region you chose - you'll need it later!

### 1.3 Complete Onboarding
- Skip the "Agent Installation" wizard (we'll do this manually)
- Skip the "Dashboard Setup" wizard (we have a custom dashboard)
- You can skip all optional steps

---

## Step 2: Get API Keys (5 minutes)

### 2.1 Get API Key
1. Log into Datadog: https://app.datadoghq.com/ (or your region)
2. Click your profile icon (bottom-left corner)
3. Select **"Organization Settings"**
4. In left menu, click **"API Keys"**
5. You'll see a default API key already created
   - Click **"Copy"** to copy the key
   - Save it temporarily in Notepad

**Alternatively, create a new API key:**
1. Click **"+ New Key"**
2. Name: "Tikun Olam - Hackathon"
3. Click **"Create Key"**
4. Copy the key value

### 2.2 Get Application Key
1. In Organization Settings, click **"Application Keys"** (in left menu)
2. Click **"+ New Key"**
3. Name: "Tikun Olam Backend"
4. Click **"Create Key"**
5. **IMPORTANT:** Copy the key immediately - it won't be shown again!
6. Save it temporarily in Notepad

### 2.3 Get RUM Application ID & Client Token (for frontend)
1. In left sidebar, go to **"UX Monitoring"** → **"RUM Applications"**
2. Click **"New Application"**
3. Choose **"React"** as the application type
4. Name: "Tikun Olam Frontend"
5. Click **"Create New RUM Application"**
6. You'll see:
   - **Application ID** (e.g., `abc123...`)
   - **Client Token** (e.g., `pub123...`)
7. Copy both values

**Summary - You should now have 4 values:**
- ✅ API Key (starts with a long random string)
- ✅ Application Key (starts with a long random string)
- ✅ RUM Application ID (short alphanumeric)
- ✅ RUM Client Token (starts with `pub`)

---

## Step 3: Configure Backend Environment (5 minutes)

### 3.1 Update .env File
Open your `.env` file in the TikunOlam root directory and add/update:

```bash
# Datadog Configuration
DATADOG_API_KEY=your-api-key-here
DATADOG_APP_KEY=your-app-key-here
DATADOG_SERVICE_NAME=tikun-olam
DATADOG_STATSD_HOST=127.0.0.1
DATADOG_STATSD_PORT=8125
DATADOG_TRACE_PORT=8126
TIKUN_ENV=development
```

**Replace:**
- `your-api-key-here` → Your API Key from Step 2.1
- `your-app-key-here` → Your Application Key from Step 2.2

### 3.2 Verify Configuration
Run this test to verify Datadog is configured:

```powershell
python -c "from monitoring.datadog_config import get_datadog_config; config = get_datadog_config(); print(f'Datadog Enabled: {config.enabled}')"
```

**Expected Output:**
```
Datadog Enabled: True
Datadog initialized successfully
```

If you see `Datadog Enabled: False`, double-check your API keys in `.env`.

---

## Step 4: Install Datadog Agent (OPTIONAL - for local development)

**Note:** This step is OPTIONAL. You can skip it and use agentless mode (metrics sent directly via API).

### Option A: Skip Agent (Recommended for Hackathon)
Your code will send metrics directly to Datadog API without a local agent.
- ✅ Easier setup
- ✅ Works immediately
- ⚠️ Some advanced tracing features may not work

### Option B: Install Agent (Full Features)
If you want full distributed tracing locally:

**Windows:**
1. Download: https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi
2. Run installer
3. Enter your API key when prompted
4. Finish installation
5. Verify: Open `http://localhost:5002` in browser

**Mac:**
```bash
DD_API_KEY=your-api-key-here DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"
```

**Linux:**
```bash
DD_API_KEY=your-api-key-here DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

---

## Step 5: Configure Frontend (5 minutes)

### 5.1 Create frontend/.env
In the `frontend/` directory, create a `.env` file:

```bash
# Datadog RUM Configuration
VITE_DATADOG_APP_ID=your-rum-app-id-here
VITE_DATADOG_CLIENT_TOKEN=your-rum-client-token-here
VITE_DATADOG_SITE=datadoghq.com
VITE_DATADOG_SERVICE=tikun-olam-frontend
VITE_DATADOG_ENV=development

# Backend API
VITE_API_URL=http://localhost:8000
```

**Replace:**
- `your-rum-app-id-here` → RUM Application ID from Step 2.3
- `your-rum-client-token-here` → RUM Client Token from Step 2.3

**Site Options:**
- US1: `datadoghq.com`
- US5: `us5.datadoghq.com`
- EU1: `datadoghq.eu`

### 5.2 Verify Frontend Configuration
```powershell
cd frontend
cat .env
```

Make sure all variables are set correctly.

---

## Step 6: Upload Dashboard to Datadog (10 minutes)

### 6.1 Run Upload Script
From the TikunOlam root directory:

```powershell
python monitoring/upload_dashboard.py
```

**Expected Output:**
```
✅ Dashboard uploaded successfully!
Dashboard ID: abc-123-def-456
Dashboard URL: https://app.datadoghq.com/dashboard/abc-123-def-456
```

**Copy the Dashboard URL** - you'll use this in your video demo!

### 6.2 View Dashboard
1. Open the dashboard URL in your browser
2. You should see 13 widgets:
   - Pipeline Execution Time
   - BinahSigma Bias Delta (KEY WIDGET)
   - Ethical Alignment Distribution
   - Decision Distribution
   - Civilizational Blind Spots
   - Active Alerts
   - Pipeline Failure Rate
   - And more...

**Note:** Widgets will be empty until you run your first analysis.

### 6.3 Troubleshooting Dashboard Upload

**Error: "Missing API key"**
- Make sure `DATADOG_API_KEY` is set in `.env`
- Verify the key is correct (no extra spaces)

**Error: "Invalid dashboard JSON"**
- This shouldn't happen - the JSON is pre-validated
- If it does, check `monitoring/datadog_dashboard.json` for syntax errors

**Error: "403 Forbidden"**
- Your API key doesn't have permission to create dashboards
- Create a new Application Key with full permissions

---

## Step 7: Create Monitoring Alerts (5 minutes)

### 7.1 Run Monitor Creation Script
```powershell
python monitoring/create_monitors.py
```

**Expected Output:**
```
✅ Created monitor: Ethical Alignment Threshold Violation (ID: 12345)
✅ Created monitor: BinahSigma Extreme Divergence (ID: 12346)
✅ Created monitor: Pipeline Performance Degradation (ID: 12347)
...
✅ All 7 monitors created successfully!
```

### 7.2 View Monitors
1. Go to Datadog: https://app.datadoghq.com/monitors/manage
2. You should see 7 new monitors:
   - **Ethical Alignment Threshold Violation** (CRITICAL)
   - **BinahSigma Extreme Divergence** (WARNING)
   - **Pipeline Performance Degradation** (WARNING)
   - **Integration Readiness Failure** (HIGH)
   - **High Pipeline Failure Rate** (CRITICAL)
   - **Keter Corruption Detection** (HIGH)
   - **Decision Confidence Drop** (MEDIUM)

---

## Step 8: Test Full Integration (10 minutes)

### 8.1 Start Backend
```powershell
uvicorn src.tikun.api.main:app --reload --port 8000
```

**Check logs for:**
```
Datadog initialized successfully
```

If you see: `Datadog not configured`, go back to Step 3.

### 8.2 Start Frontend
```powershell
cd frontend
npm run dev
```

**Check browser console for:**
```
Datadog RUM initialized
```

### 8.3 Run Test Analysis
1. Open http://localhost:5173
2. Enter this scenario:
   ```
   A city council is considering implementing a universal basic income (UBI)
   program funded by a 2% tax on automated services. The program would provide
   $1000/month to all residents earning less than $50,000/year.
   ```
3. Case name: "test_datadog"
4. Click **"Analyze Scenario"**
5. Wait for analysis to complete (~30-60 seconds)

### 8.4 Verify Metrics in Datadog

**Wait 2-3 minutes for metrics to appear**, then:

1. Go to your Datadog dashboard URL (from Step 6.1)
2. Refresh the page
3. You should see data in the widgets:
   - **Pipeline Execution Time:** ~30-60 seconds
   - **Ethical Alignment:** ~85-95%
   - **BinahSigma Bias Delta:** Should show a percentage
   - **Decision:** Should show GO/NO-GO/CONDITIONAL

**If you see "No data":**
- Wait 5 more minutes (metrics can take time to appear)
- Check backend logs for errors
- Verify API keys are correct
- Try running another analysis

### 8.5 Check RUM Data
1. Go to: https://app.datadoghq.com/rum/explorer
2. Filter by: `service:tikun-olam-frontend`
3. You should see:
   - Page views
   - User interactions (button clicks)
   - Performance metrics

---

## Step 9: Take Screenshots for Video (5 minutes)

Now that everything is working, take screenshots for your hackathon video:

### Screenshots to Capture:

**1. Main Dashboard**
- URL: Your Datadog dashboard URL
- Make sure all widgets show data
- Use Windows Snipping Tool (Win + Shift + S)
- Save as: `docs/screenshots/datadog-dashboard.png`

**2. BinahSigma Widget (Close-up)**
- Zoom in on the "BinahSigma Bias Delta" widget
- Show the percentage clearly
- Save as: `docs/screenshots/binah-sigma-metric.png`

**3. Trace View (if available)**
- Go to: https://app.datadoghq.com/apm/traces
- Filter by: `service:tikun-olam`
- Open a trace to show all 10 Sefirot spans
- Save as: `docs/screenshots/trace-view.png`

**4. Active Monitors**
- Go to: https://app.datadoghq.com/monitors/manage
- Show the 7 monitors you created
- Save as: `docs/screenshots/monitors.png`

**Tips:**
- Use 1920x1080 resolution for best quality
- Make sure text is readable
- Hide any sensitive information (account email, etc.)

---

## Step 10: Configure for Cloud Run (Optional)

If you're deploying to Cloud Run, you need to add secrets:

### 10.1 Create Secrets in Google Cloud
```powershell
# Set project
gcloud config set project algebraic-craft-453221-g1

# Create Datadog API Key secret
echo "your-api-key-here" | gcloud secrets create DATADOG_API_KEY --data-file=-

# Create Datadog App Key secret
echo "your-app-key-here" | gcloud secrets create DATADOG_APP_KEY --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding DATADOG_API_KEY \
  --member="serviceAccount:algebraic-craft-453221-g1@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding DATADOG_APP_KEY \
  --member="serviceAccount:algebraic-craft-453221-g1@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

The `cloudbuild.yaml` is already configured to use these secrets!

---

## Configuration Summary Checklist

After completing all steps, verify:

### Backend:
- [ ] `.env` file has `DATADOG_API_KEY` and `DATADOG_APP_KEY`
- [ ] Running `python -c "from monitoring.datadog_config import get_datadog_config; print(get_datadog_config().enabled)"` returns `True`
- [ ] Backend starts without "Datadog not configured" warning

### Frontend:
- [ ] `frontend/.env` has `VITE_DATADOG_APP_ID` and `VITE_DATADOG_CLIENT_TOKEN`
- [ ] Browser console shows "Datadog RUM initialized"
- [ ] No errors in browser console related to Datadog

### Datadog:
- [ ] Dashboard created and accessible via URL
- [ ] 7 monitors created in Monitors page
- [ ] RUM application visible in UX Monitoring
- [ ] Can see metrics after running test analysis

### Screenshots:
- [ ] Dashboard screenshot taken (1920x1080)
- [ ] BinahSigma widget screenshot taken
- [ ] Monitors screenshot taken
- [ ] All screenshots saved in `docs/screenshots/`

---

## Common Issues & Solutions

### Issue 1: "Datadog not configured" in logs
**Solution:**
- Check `.env` file exists in root directory
- Verify `DATADOG_API_KEY` and `DATADOG_APP_KEY` are set
- Make sure there are no quotes around the keys
- Restart backend after updating `.env`

### Issue 2: No metrics appearing in dashboard
**Solution:**
- Wait 5-10 minutes (Datadog has ingestion delay)
- Check backend logs for metric emission
- Verify API key is correct
- Try running another analysis
- Check if agent is running (if you installed it)

### Issue 3: "Invalid API Key" error
**Solution:**
- Copy-paste the API key again (no extra spaces)
- Make sure you're using the right region (US1 vs US5)
- Try creating a new API key

### Issue 4: Dashboard upload fails
**Solution:**
- Verify Application Key has dashboard creation permissions
- Check `monitoring/datadog_dashboard.json` is valid JSON
- Try manual upload: Copy JSON content and paste in Datadog UI

### Issue 5: Frontend RUM not working
**Solution:**
- Check `frontend/.env` exists (not `.env.example`)
- Verify `VITE_DATADOG_APP_ID` and `VITE_DATADOG_CLIENT_TOKEN` are correct
- Restart frontend dev server after updating `.env`
- Check browser console for Datadog errors

---

## Cost Information

### Free Trial:
- **Duration:** 14 days
- **Features:** Full platform access
- **Hosts:** Unlimited
- **Metrics:** Unlimited custom metrics
- **Logs:** 15-day retention
- **RUM:** 10,000 sessions included
- **Credit Card:** NOT required

**For this hackathon:**
- You'll use < 5% of free trial limits
- Total cost: **$0.00**

### After Trial:
If you continue using Datadog after the hackathon:
- **Infrastructure:** $15/host/month (can pause anytime)
- **APM:** $31/host/month
- **RUM:** $15/10K sessions
- **Free Tier:** Available for small projects

**Recommendation:** Cancel before trial ends if you don't need it.

---

## Video Demo Preparation

### What to Show in Video:

**1. Dashboard Overview (20 seconds)**
- Full dashboard with all widgets
- Point out: "13 widgets monitoring ethical AI in real-time"
- Highlight the BinahSigma Bias Delta widget

**2. BinahSigma Metric (10 seconds)**
- Zoom in on bias_delta percentage
- Explain: "52% civilizational divergence - Western vs Eastern AI"

**3. Alerts (10 seconds)**
- Show monitors page
- Explain: "7 alerts monitoring ethical violations"

**4. Live Analysis (optional)**
- Run analysis and show metrics updating
- This is impressive but requires good timing

**Tips:**
- Use high-resolution screen capture (1080p)
- Prepare dashboard in separate browser tab
- Practice transitions between frontend and Datadog
- Have dashboard already loaded before recording

---

## Next Steps

Once Datadog is fully configured:

1. ✅ **Practice your demo** - run analyses and watch metrics
2. ✅ **Take screenshots** - all widgets should have data
3. ✅ **Record video** - show dashboard in action
4. ✅ **Document in README** - add dashboard URL
5. ✅ **Submit to Devpost** - emphasize observability in description

---

## Support Resources

### Datadog Documentation:
- Dashboard API: https://docs.datadoghq.com/api/latest/dashboards/
- Custom Metrics: https://docs.datadoghq.com/metrics/custom_metrics/
- RUM Setup: https://docs.datadoghq.com/real_user_monitoring/
- APM Python: https://docs.datadoghq.com/tracing/setup_overview/setup/python/

### Datadog Support:
- Community: https://datadoghq.slack.com/
- Docs: https://docs.datadoghq.com/
- Support: support@datadoghq.com (Pro/Enterprise only)

### Tikun Olam Datadog Files:
- Config: `monitoring/datadog_config.py`
- Dashboard: `monitoring/datadog_dashboard.json`
- Monitors: `monitoring/detection_rules.py`
- Upload Scripts: `monitoring/upload_dashboard.py`, `monitoring/create_monitors.py`

---

**Congratulations!** 🎉

You now have **full production-grade observability** for your ethical AI system.

This is a **MASSIVE differentiator** for the hackathon. Very few projects will have this level of monitoring and instrumentation.

**Your competitive advantages:**
1. ✅ BinahSigma bias_delta metric (unique to your project)
2. ✅ Custom dashboard with 13 widgets
3. ✅ 7 intelligent monitors for ethical violations
4. ✅ Full distributed tracing across 10 Sefirot
5. ✅ Frontend RUM for user experience monitoring

**Now go record an amazing video showcasing this observability!** 🚀📹

---

**Last Updated:** December 24, 2025
**Next Step:** Record video demo (VIDEO_DEMO_SCRIPT.md)
**Deadline:** December 31, 2025 @ 4:00pm CST
