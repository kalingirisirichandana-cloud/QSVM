# Deployment Guide for Render

This guide provides step-by-step instructions for deploying the QSVM Fraud Detection application on Render.

## Quick Deploy Checklist

- [ ] Code pushed to GitHub repository
- [ ] Render account created
- [ ] creditcard.csv file ready (144MB dataset)
- [ ] Repository connected to Render

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure all files are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up (GitHub OAuth recommended)
3. Verify your email if required

### 3. Deploy via Dashboard

1. **Navigate to Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create New Web Service**
   - Click the "New +" button
   - Select "Web Service"

3. **Connect Repository**
   - Click "Connect account" if not already connected
   - Authorize Render to access your GitHub repositories
   - Select your repository: `kalingirisirichandana-cloud/QSVM`

4. **Configure Service**
   - **Name**: `qsvm-fraud-detection` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

5. **Set Environment Variables** (Optional)
   - `FLASK_DEBUG`: `False`
   - `PYTHON_VERSION`: `3.11.6`

6. **Select Plan**
   - **Free**: Good for testing (spins down after 15 min inactivity)
   - **Starter** ($7/mo): Better performance, always on
   - **Standard** ($25/mo): Production-ready

7. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (first build: 5-10 minutes)

### 4. Upload Dataset File

⚠️ **Important**: The `creditcard.csv` file (144MB) needs to be uploaded separately.

**Option A: Using Render Shell (Recommended)**

1. In your service dashboard, go to "Shell" tab
2. Run:
   ```bash
   curl -O https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/download
   ```
   Or upload manually via:
   ```bash
   # In Render Shell, you can use wget or curl to download
   # Or use Render's file upload feature if available
   ```

**Option B: Using Render Console/SSH**

1. Enable SSH access in your service settings
2. Use SFTP or SCP to upload the file:
   ```bash
   scp creditcard.csv <your-service>:/opt/render/project/src/
   ```

**Option C: Using Git LFS (Advanced)**

1. Install Git LFS: `git lfs install`
2. Track the CSV: `git lfs track "*.csv"`
3. Add and commit: `git add .gitattributes creditcard.csv && git commit -m "Add dataset via LFS"`
4. Push: `git push origin main`

### 5. Verify Deployment

1. Visit your service URL (e.g., `https://qsvm-fraud-detection.onrender.com`)
2. You should see the homepage with the fraud detection form
3. Test a prediction:
   - V1: `-1.359807`
   - V2: `-0.072781`
   - Click "Predict Fraud Status"

### 6. Monitor Your Service

- **Logs**: View real-time logs in the "Logs" tab
- **Metrics**: Monitor CPU, memory usage in "Metrics" tab
- **Events**: Track deployments and errors in "Events" tab

## Troubleshooting

### Build Fails

- **Check logs**: Look for error messages in build logs
- **Dependencies**: Ensure `requirements.txt` is correct
- **Python version**: Verify `runtime.txt` specifies correct version

### Service Crashes

- **Check logs**: Look for Python errors
- **Dataset missing**: Ensure `creditcard.csv` is in root directory
- **Memory issues**: Consider upgrading plan or reducing sample size

### Slow Performance

- **Free tier**: Services spin down after inactivity (15 min)
- **Cold starts**: First request after spin-down takes 30-60 seconds
- **Model training**: First run trains model (5-10 minutes)
- **Solution**: Upgrade to paid plan for always-on service

### Dataset Not Found

- **Check file location**: Must be in project root
- **File permissions**: Ensure file is readable
- **File name**: Must be exactly `creditcard.csv`

## Environment Variables

Optional environment variables you can set:

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_DEBUG` | `False` | Disable debug mode for production |
| `PYTHON_VERSION` | `3.11.6` | Python version (also in runtime.txt) |
| `PORT` | Auto | Port number (automatically set by Render) |

## Updating Your Deployment

After making changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update application"
   git push origin main
   ```

2. Render will automatically detect changes and redeploy

3. Monitor deployment in Render Dashboard

## Cost Considerations

- **Free Tier**: 
  - Spins down after 15 minutes of inactivity
  - 750 hours/month free
  - Suitable for demos and testing
  
- **Paid Plans**:
  - Always-on service
  - Better performance
  - More resources
  - Recommended for production

## Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **Project Issues**: Open an issue in your GitHub repository



