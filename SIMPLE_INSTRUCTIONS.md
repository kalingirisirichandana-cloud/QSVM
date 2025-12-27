# 🚀 Simple Instructions - Get Your App Working!

## Step-by-Step Guide (Super Easy!)

### Step 1: Upload Your Dataset to Google Drive

1. **Go to Google Drive**: https://drive.google.com
2. **Upload the file**:
   - Click "New" button (top left)
   - Click "File upload"
   - Select `creditcard.csv` from `/home/rgukt/Documents/QSVM/`
   - Wait for upload to finish

3. **Get a Shareable Link**:
   - Right-click on `creditcard.csv` in Google Drive
   - Click "Share" → "Get link"
   - Make sure it's set to "Anyone with the link"
   - Copy the link (it looks like: `https://drive.google.com/file/d/XXXXX/view?usp=sharing`)

4. **Convert to Direct Download Link**:
   - The link you have is a viewing link, we need a download link
   - Replace `/view?usp=sharing` with `/uc?export=download&id=`
   - Example: If your link is:
     ```
     https://drive.google.com/file/d/1ABC123XYZ789/view?usp=sharing
     ```
     Change it to:
     ```
     https://drive.google.com/uc?export=download&id=1ABC123XYZ789
     ```
   - The ID is the part between `/d/` and `/view`

### Step 2: Add the Link to Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click on your service** (the one showing "Model Not Ready")
3. **Click "Environment"** tab (left sidebar)
4. **Click "Add Environment Variable"**
5. **Add this**:
   - **Key**: `DATASET_URL`
   - **Value**: Paste your Google Drive download link from Step 1
6. **Click "Save Changes"**

### Step 3: Restart Your Service

1. **Still in Render Dashboard**, click **"Manual Deploy"** (top right)
2. **Click "Deploy latest commit"**
3. **Wait 2-3 minutes** for it to restart

### Step 4: Check if It Works!

1. **Click "Logs"** tab in Render Dashboard
2. **Look for**: "Successfully downloaded creditcard.csv"
3. **Then look for**: "Model initialized successfully!"
4. **Visit your website** - the warning should be gone! 🎉

---

## That's It! 🎊

If you see "Model initialized successfully!" in the logs, you're done!

Try making a prediction:
- V1: `-1.359807`
- V2: `-0.072781`
- Click "Predict Fraud Status"

---

## Still Having Trouble?

### The Google Drive Link Didn't Work?

Try this alternative: **Use Dropbox**

1. Upload `creditcard.csv` to Dropbox
2. Right-click → Share → Copy link
3. Change `www.dropbox.com` to `dl.dropboxusercontent.com` in the URL
4. Remove `?dl=0` from the end if it's there
5. Use this as your `DATASET_URL` in Render

### Need Help?

Check the logs in Render Dashboard to see what error message appears. Common issues:
- "File too small" - The download didn't work, try a different link
- "Could not download" - Check your DATASET_URL is correct
- "Model initialized successfully!" - You're good! ✅

