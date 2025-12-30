# Vertex AI Setup Guide for Tikun Olam

## Quick Setup (5 minutes)

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Note your **Project ID** (not the project name)

### 2. Enable Vertex AI API

```bash
# Option A: Using gcloud CLI
gcloud services enable aiplatform.googleapis.com

# Option B: Via Console
# Go to: https://console.cloud.google.com/apis/library/aiplatform.googleapis.com
# Click "Enable"
```

### 3. Set Up Authentication

**Option A: Application Default Credentials (Recommended for local testing)**

```bash
gcloud auth application-default login
```

**Option B: Service Account (Recommended for production)**

1. Create service account:
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
   - Click "Create Service Account"
   - Name: `tikun-olam-vertex`
   - Grant role: `Vertex AI User`

2. Create and download JSON key:
   - Click on the service account
   - Go to "Keys" tab
   - "Add Key" → "Create new key" → JSON
   - Save as `vertex-ai-key.json` in project root

3. Set environment variable:
   ```bash
   # Windows
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\vertex-ai-key.json

   # Linux/Mac
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/vertex-ai-key.json
   ```

### 4. Update .env File

```bash
# Replace with your actual project ID
GCP_PROJECT_ID=your-actual-project-id

# Region (us-central1 is recommended)
GCP_LOCATION=us-central1
```

### 5. Test the Migration

```bash
python test_vertex_migration.py
```

Expected output:
```
🚀 TIKUN OLAM - VERTEX AI MIGRATION TEST

================================================================================
TEST 1: Vertex AI Initialization
================================================================================
✅ GCP Project ID: your-project-id
✅ GCP Location: us-central1
✅ Keter Model: gemini-1.5-pro

================================================================================
TEST 2: Keter Vertex AI Integration
================================================================================
✅ Keter initialized successfully

Testing scenario:
A city council is considering implementing a universal basic income (UBI)...

Calling Vertex AI via Keter...

✅ Vertex AI call successful!

Results:
  • Alignment: 78%
  • Corruption: low
  • Manifestation Valid: True
  • Threshold Met: True

✅ Response structure validated

🎉 ALL CRITICAL TESTS PASSED!
```

## Troubleshooting

### Error: "GCP_PROJECT_ID not configured"
- Make sure you updated `.env` with your actual project ID
- Restart your terminal/IDE after updating `.env`

### Error: "Permission denied" or "API not enabled"
- Enable Vertex AI API: `gcloud services enable aiplatform.googleapis.com`
- Verify your account has Vertex AI User role

### Error: "Could not automatically determine credentials"
- Run: `gcloud auth application-default login`
- Or set `GOOGLE_APPLICATION_CREDENTIALS` to your service account JSON

### Error: "Model not found: gemini-1.5-pro"
- Verify Vertex AI API is enabled
- Check that your project has access to Gemini models
- Some regions may not have all models - try `us-central1`

## Cost Considerations

**Vertex AI Pricing (as of 2025):**
- Gemini 1.5 Pro: ~$0.00125 per 1K input tokens, ~$0.005 per 1K output tokens
- Each Tikun analysis: ~10-20 API calls (one per Sefira)
- Estimated cost per analysis: $0.10 - $0.50

**For Hackathon:**
- Google Cloud offers $300 free credits for new accounts
- This is more than enough for testing and demo purposes

## Next Steps

Once tests pass:
1. ✅ Vertex AI migration complete
2. ✅ Ready for full pipeline testing
3. ✅ Can deploy to Cloud Run
4. Configure Datadog for observability (see DATADOG_SETUP.md)
