import boto3
import pandas as pd
from io import StringIO

# ✅ S3 Bucket and File Paths
s3_bucket = "dmmlassignment"
s3_input_key = "dmmlassignment-customer-churn/customer_churn_data.csv"
s3_output_key = "dmmlassignment-customer-churn/cleaned_customer_churn_data.csv"

# Initialize S3 client
s3 = boto3.client("s3")

# Fetch file from S3
response = s3.get_object(Bucket=s3_bucket, Key=s3_input_key)
df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

# ✅ 1. Basic EDA - Print column info
print("Dataset Overview:")
print(df.info())
print(df.describe())

# ✅ 2. Handling Missing Values
df.fillna(df.median(numeric_only=True), inplace=True)  # Fill missing numerical values with median
df.fillna("Unknown", inplace=True)  # Fill categorical missing values with "Unknown"

# ✅ 3. Feature Engineering (Example: Convert categorical to numerical)
if "gender" in df.columns:
    df["gender"] = df["gender"].map({"Male": 1, "Female": 0})

# ✅ 4. Save the cleaned dataset back to S3
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
s3.put_object(Bucket=s3_bucket, Key=s3_output_key, Body=csv_buffer.getvalue())

print("✅ Data preparation complete. Cleaned data uploaded to S3:", s3_output_key)

