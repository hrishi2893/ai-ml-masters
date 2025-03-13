import boto3
import json

# ✅ S3 Configuration
s3_bucket = "dmmlassignment"
s3_metadata_key = "dmmlassignment-customer-churn/feature_store_metadata.json"

# ✅ Feature Metadata
feature_metadata = {
    "customer_tenure_days": {
        "description": "Number of days since customer signup",
        "source": "Calculated from signup_date",
        "version": "1.0"
    },
    "avg_transaction_value": {
        "description": "Average transaction value of a customer",
        "source": "Derived from total_spend and num_transactions",
        "version": "1.0"
    }
}

# ✅ Convert metadata to JSON
metadata_json = json.dumps(feature_metadata, indent=4)

# ✅ Upload to S3
s3 = boto3.client("s3")
s3.put_object(Bucket=s3_bucket, Key=s3_metadata_key, Body=metadata_json)

print(f"✅ Feature metadata uploaded to S3: s3://{s3_bucket}/{s3_metadata_key}")

