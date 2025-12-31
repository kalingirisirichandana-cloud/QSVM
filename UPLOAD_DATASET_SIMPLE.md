# Quick Fix: Upload creditcard.csv to Render

## The Problem
Your app shows "Model Not Ready" because the `creditcard.csv` file (144MB) is missing on the Render server.

## Quick Solution: Upload via Render Shell

### Step 1: Get your local creditcard.csv file ready
Make sure you have the `creditcard.csv` file on your local computer (in `/home/rgukt/Documents/QSVM/`).

### Step 2: Open Render Shell
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click on your service name (e.g., `qsvm-fraud-detection`)
3. Click on the **"Shell"** tab (left sidebar)
4. Wait for the terminal to open

### Step 3: Upload the file using Python HTTP server (Easiest method)

**On your local computer:**
```bash
cd /home/rgukt/Documents/QSVM
python3 -m http.server 8000
```
Keep this terminal open - it's serving the file.

**In Render Shell:**
```bash
cd /opt/render/project/src  # or wherever your app is deployed
curl -O http://YOUR_LOCAL_IP:8000/creditcard.csv
```

**To find your local IP:**
```bash
# On your local computer, run:
hostname -I
# or
ip addr show
```

### Alternative: Use base64 encoding (if above doesn't work)

**On your local computer:**
```bash
cd /home/rgukt/Documents/QSVM
base64 creditcard.csv > creditcard.csv.base64
# Then copy the content and paste in Render Shell
```

**In Render Shell:**
```bash
# Paste the base64 content into a file
nano creditcard.csv.base64
# Then decode it
base64 -d creditcard.csv.base64 > creditcard.csv
rm creditcard.csv.base64
```

### Alternative: Use wget/curl with a cloud storage service

1. Upload `creditcard.csv` to Google Drive, Dropbox, or similar
2. Get a direct download link
3. In Render Shell:
```bash
cd /opt/render/project/src
wget "YOUR_DOWNLOAD_LINK" -O creditcard.csv
# or
curl -L "YOUR_DOWNLOAD_LINK" -o creditcard.csv
```

### Step 4: Verify the file
In Render Shell:
```bash
ls -lh creditcard.csv
# Should show ~144MB file
```

### Step 5: Restart your service
1. Go back to Render Dashboard
2. Click "Manual Deploy" → "Deploy latest commit"
3. Or the service will auto-restart if you made changes

### Step 6: Check logs
After restart, check the logs to see if the model initializes:
- Click "Logs" tab in Render Dashboard
- Look for "Model initialized successfully!"

## Quick Method: Using Render's Persistent Disk (Paid Plans)

If you're on a paid plan, you can enable persistent disk storage and the file will persist across deployments.

## Troubleshooting

**File too large?**
- The file is 144MB, which should work fine
- If upload fails, try splitting or using a different method

**Can't access Shell?**
- Make sure your service is running
- Try restarting the service first

**File uploads but model still not ready?**
- Check file permissions: `chmod 644 creditcard.csv`
- Check file location: Should be in project root (same directory as `app.py`)
- Check logs for specific error messages



