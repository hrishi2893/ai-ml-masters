import boto3
import pandas as pd
from io import StringIO

# ✅ S3 Configuration
s3_bucket = "dmmlassignment"
s3_transformed_data_key = "dmmlassignment-customer-churn/transformed_customer_churn_data.csv"

# ✅ Initialize S3 client
s3 = boto3.client("s3")

def get_features(feature_names):
    """Retrieve selected features from the transformed dataset in S3."""
    response = s3.get_object(Bucket=s3_bucket, Key=s3_transformed_data_key)
    df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

    # ✅ Print available columns for debugging
    print("Available Features in Dataset:", df.columns.tolist())

    # ✅ Ensure all requested features exist
    missing_features = [f for f in feature_names if f not in df.columns]
    if missing_features:
        print(f"⚠ Missing features: {missing_features}")
        return None

    return df[feature_names]

# ✅ Example Usage
if __name__ == "__main__":
    features = ["customer_tenure_days", "avg_transaction_value"]  # Check these names in your dataset
    retrieved_data = get_features(features)
    
    if retrieved_data is not None:
        print("✅ Sample Retrieved Features:\n", retrieved_data.head())
    else:
        print("❌ No data retrieved. Check feature names!")

