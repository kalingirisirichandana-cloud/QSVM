#!/usr/bin/env python3
"""
Script to download the creditcard.csv dataset.
Can be run during Render build or manually.

This script attempts to download the dataset from Kaggle or a backup source.
"""

import os
import sys
import urllib.request
import zipfile

DATASET_URL = "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/download"
DATASET_FILE = "creditcard.csv"
BACKUP_URLS = [
    # Add backup URLs here if available
    # Example: "https://example.com/datasets/creditcard.csv"
]


def download_from_url(url, output_file):
    """Download file from URL."""
    try:
        print(f"Attempting to download from {url}...")
        urllib.request.urlretrieve(url, output_file)
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Successfully downloaded {output_file}")
            return True
    except Exception as e:
        print(f"Failed to download from {url}: {e}")
        return False
    return False


def download_from_kaggle():
    """Download dataset using Kaggle API (requires credentials)."""
    try:
        import kaggle
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        # Download the dataset
        api.dataset_download_files('mlg-ulb/creditcardfraud', path='.', unzip=True)
        
        if os.path.exists(DATASET_FILE):
            print(f"Successfully downloaded {DATASET_FILE} using Kaggle API")
            return True
    except ImportError:
        print("Kaggle API not installed. Install with: pip install kaggle")
    except Exception as e:
        print(f"Failed to download using Kaggle API: {e}")
    
    return False


def main():
    """Main function to download the dataset."""
    if os.path.exists(DATASET_FILE):
        print(f"{DATASET_FILE} already exists. Skipping download.")
        return 0
    
    print("=" * 50)
    print("Downloading creditcard.csv dataset...")
    print("=" * 50)
    
    # Try Kaggle API first (if credentials are set)
    if download_from_kaggle():
        return 0
    
    # Try backup URLs
    for url in BACKUP_URLS:
        if download_from_url(url, DATASET_FILE):
            return 0
    
    print("=" * 50)
    print("ERROR: Could not download dataset automatically.")
    print("Please download manually from:")
    print("https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
    print("And upload it to your Render server using the Shell.")
    print("=" * 50)
    return 1


if __name__ == "__main__":
    sys.exit(main())



