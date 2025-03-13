import boto3
import pandas as pd
from io import StringIO

# ✅ S3 Bucket and File Paths
s3_bucket = "dmmlassignment"
s3_input_key = "dmmlassignment-customer-churn/cleaned_customer_churn_data.csv"
s3_output_key = "dmmlassignment-customer-churn/transformed_customer_churn_data.csv"

# Initialize S3 client
s3 = boto3.client("s3")

# ✅ 1. Load cleaned data from S3
response = s3.get_object(Bucket=s3_bucket, Key=s3_input_key)
df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

# ✅ 2. Ensure `TotalCharges` is numeric
if "TotalCharges" in df.columns:
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")  # Convert to float, set errors to NaN
    df["TotalCharges"].fillna(0, inplace=True)  # Replace NaNs with 0
else:
    print("⚠ 'TotalCharges' column missing!")

# ✅ 3. Feature Engineering (Fixing Missing Features)
if "tenure" in df.columns:
    df["customer_tenure_days"] = df["tenure"] * 30  # Convert tenure from months to days
else:
    print("⚠ 'tenure' column missing!")

if "MonthlyCharges" in df.columns and "TotalCharges" in df.columns:
    df["avg_transaction_value"] = df["TotalCharges"] / (df["tenure"] + 1)  # Avoid division by zero
    df["avg_transaction_value"].fillna(0, inplace=True)
else:
    print("⚠ 'MonthlyCharges' or 'TotalCharges' column missing!")

# ✅ 4. Save transformed dataset back to S3
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
s3.put_object(Bucket=s3_bucket, Key=s3_output_key, Body=csv_buffer.getvalue())

print("✅ Data transformation complete. Transformed data uploaded to S3:", s3_output_key)

