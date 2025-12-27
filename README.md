# QSVM Fraud Detection Web Application

A Flask-based web application that uses a Quantum Support Vector Machine (QSVM) for credit card fraud detection. The application provides an intuitive web interface to predict fraud for individual transactions or batch process CSV files.

## Features

- **Quantum Machine Learning**: Uses Qiskit Machine Learning with Quantum Kernels for fraud detection
- **Web Interface**: Simple and clean web UI for easy interaction
- **Single Transaction Prediction**: Enter V1 and V2 feature values to get instant predictions
- **Batch Processing**: Upload CSV files to process multiple transactions at once
- **Model Persistence**: Trained models are saved and reused (no retraining needed on restart)
- **Kaggle Dataset Compatible**: Works with the standard Kaggle creditcard.csv format

## Project Structure

```
QSVM/
├── app.py                 # Flask application with routes
├── qsvm_model.py          # QSVM model training and prediction logic
├── creditcard.csv         # Dataset file (must be present)
├── templates/
│   ├── index.html         # Homepage with input forms
│   └── result.html        # Results display page
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Prerequisites

- Python 3.9 or higher
- creditcard.csv dataset file (from Kaggle)
- Internet connection (for initial Qiskit setup, if needed)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd QSVM
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the dataset file is present:**
   Make sure `creditcard.csv` is in the project root directory. If you don't have it, download it from:
   [Kaggle Credit Card Fraud Detection Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

## Running the Application

### Method 1: Using Python directly
```bash
python app.py
```

### Method 2: Using Flask CLI
```bash
flask run
```

The application will:
1. Check if a trained model exists
2. If not found, train a new QSVM model (this may take a few minutes)
3. Start the Flask server

Once running, open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Deployment on Render

This application is ready to deploy on [Render](https://render.com), a cloud platform for hosting web applications.

### Prerequisites for Render Deployment

1. **GitHub Repository**: Your code should be pushed to a GitHub repository (already done!)
2. **Render Account**: Sign up for a free account at [render.com](https://render.com)

### Deployment Steps

#### Option 1: Using Render Dashboard (Recommended)

1. **Log in to Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create a free account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account if not already connected
   - Select your repository: `kalingirisirichandana-cloud/QSVM`

3. **Configure the Service**
   - **Name**: `qsvm-fraud-detection` (or any name you prefer)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (root directory)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Environment Variables** (Optional)
   - `FLASK_DEBUG`: `False` (for production)
   - `PYTHON_VERSION`: `3.11.6` (optional, specified in runtime.txt)

5. **Plan Selection**
   - **Free Tier**: Suitable for testing and demos
   - **Starter/Standard**: Better performance for production use

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - First deployment may take 10-15 minutes (model training)
   - You'll get a URL like: `https://qsvm-fraud-detection.onrender.com`

#### Option 2: Using Render Blueprint (render.yaml)

If you prefer infrastructure-as-code:

1. The project includes a `render.yaml` file
2. In Render Dashboard, click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect and use `render.yaml`
5. Review and deploy

### Important Notes for Render Deployment

⚠️ **Dataset File (creditcard.csv)**:
- The dataset file (144MB) is **NOT included** in the repository (too large for Git)
- **Option A**: Upload via Render Shell/Console after deployment
  - Use Render's web console or SSH to upload the file
- **Option B**: Use Render Disk Storage
  - Enable persistent disk storage in your service settings
  - Upload the file after first deployment
- **Option C**: Download during build (advanced)
  - Add build command to download from a cloud storage service

📝 **Model Training**:
- On first deployment, the model will train (takes 5-10 minutes)
- Subsequent deployments will reuse the trained model (faster)
- Model files (`.pkl`) are saved to disk and persist across restarts

⚡ **Performance**:
- Free tier services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds (cold start)
- Consider upgrading to a paid plan for always-on service

### Verify Deployment

1. Visit your Render URL (e.g., `https://your-app.onrender.com`)
2. The homepage should load with the fraud detection form
3. Test with sample V1 and V2 values (e.g., V1=-1.36, V2=-0.073)

### Monitoring

- **Logs**: View real-time logs in Render Dashboard
- **Metrics**: Monitor CPU, memory, and request metrics
- **Events**: Track deployment events and errors

## Usage

### Single Transaction Prediction

1. On the homepage, enter values for:
   - **V1**: First PCA-transformed feature value
   - **V2**: Second PCA-transformed feature value
2. Click "Predict Fraud Status"
3. View the prediction result (Fraud or Not Fraud)

### Batch Prediction (CSV Upload)

1. Prepare a CSV file with at least `V1` and `V2` columns
2. The CSV can include additional columns (Time, Amount, Class, etc.) which will be displayed but not used for prediction
3. Click "Choose File" and select your CSV
4. Click "Predict Batch Transactions"
5. View the results table with predictions for all transactions

### CSV Format Example

```csv
Time,V1,V2,V3,Amount,Class
0,-1.359807,-0.072781,2.536347,149.62,0
0,1.191857,0.266151,0.166480,2.69,0
```

**Required columns:** `V1`, `V2`  
**Optional columns:** Any other columns will be preserved in the output

## Model Details

The QSVM model:
- Uses **V1 and V2** features only (2-dimensional feature space)
- Uses a **ZZFeatureMap** with 2 repetitions
- Uses **FidelityQuantumKernel** for quantum kernel computation
- Uses **scikit-learn SVC** with precomputed kernel
- Trains on a balanced sample (50 fraud + 50 normal transactions by default)
- Model files are saved as pickle files for reuse:
  - `qsvm_model.pkl` - Trained SVC model
  - `quantum_kernel.pkl` - Quantum kernel
  - `feature_map.pkl` - Feature map
  - `X_train.pkl` - Training features

## API Endpoint

The application also provides a JSON API endpoint for programmatic access:

**POST** `/api/predict`

Request body:
```json
{
    "v1": -1.359807,
    "v2": -0.072781
}
```

Response:
```json
{
    "v1": -1.359807,
    "v2": -0.072781,
    "prediction": "Not Fraud",
    "prediction_code": 0,
    "confidence": null
}
```

## Notes

- The first run will train the model, which may take a few minutes
- Subsequent runs will load the saved model (much faster startup)
- The model uses a small sample for training to keep computation time reasonable
- For production use, consider training on larger datasets or fine-tuning hyperparameters
- Quantum kernel computation can be slow for large batches

## Troubleshooting

**Model training fails:**
- Ensure `creditcard.csv` is in the project root directory
- Check that the CSV file is valid and contains the required columns (V1, V2, Class)

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're using the correct Python version (3.9+)

**Port already in use:**
- The default port is 5000. Change it in `app.py` or use: `flask run --port 5001`

**Model files corrupted:**
- Delete the `.pkl` files (`qsvm_model.pkl`, `quantum_kernel.pkl`, `feature_map.pkl`, `X_train.pkl`) to force retraining

## License

This project is provided as-is for educational and demonstration purposes.

## Acknowledgments

- Dataset: [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- Qiskit: [IBM Qiskit](https://qiskit.org/)
- Flask: [Flask Web Framework](https://flask.palletsprojects.com/)
