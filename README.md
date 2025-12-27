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
