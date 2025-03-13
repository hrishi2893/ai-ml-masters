import boto3
import pandas as pd
from io import StringIO
from datetime import datetime

# ✅ S3 Bucket and File Paths
s3_bucket = "dmmlassignment"
s3_input_key = "dmmlassignment-customer-churn/cleaned_customer_churn_data.csv"
s3_output_key = "dmmlassignment-customer-churn/transformed_customer_churn_data.csv"

# Initialize S3 client
s3 = boto3.client("s3")

# ✅ 1. Load cleaned data from S3
response = s3.get_object(Bucket=s3_bucket, Key=s3_input_key)
df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

# ✅ 2. Feature Engineering
if "signup_date" in df.columns:
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["customer_tenure_days"] = (datetime.now() - df["signup_date"]).dt.days

if "total_spend" in df.columns and "num_transactions" in df.columns:
    df["avg_transaction_value"] = df["total_spend"] / df["num_transactions"]
    df["avg_transaction_value"].fillna(0, inplace=True)  # Handle division by zero

# ✅ 3. Scaling/Normalization (Min-Max Scaling)
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[num_cols] = (df[num_cols] - df[num_cols].min()) / (df[num_cols].max() - df[num_cols].min())

# ✅ 4. Save transformed dataset back to S3
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
s3.put_object(Bucket=s3_bucket, Key=s3_output_key, Body=csv_buffer.getvalue())

print(f"✅ Data transformation complete. Transformed data uploaded to S3: s3://{s3_bucket}/{s3_output_key}")

