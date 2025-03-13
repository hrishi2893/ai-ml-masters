import boto3
import pandas as pd
from io import StringIO
import json

# ✅ Correct S3 Bucket and Key
s3_bucket = "dmmlassignment"
s3_key = "dmmlassignment-customer-churn/customer_churn_data.csv"
s3_output_key = "dmmlassignment-customer-churn/validation_report.json"

# Initialize S3 client
s3 = boto3.client("s3")

# Fetch file from S3
response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

# ✅ Manual Data Validation (Replacing Great Expectations)
validation_results = {}

# Check if "customer_id" column exists and has no nulls
if "customer_id" in df.columns:
    validation_results["customer_id_exists"] = True
    validation_results["customer_id_no_nulls"] = df["customer_id"].isnull().sum() == 0
else:
    validation_results["customer_id_exists"] = False
    validation_results["customer_id_no_nulls"] = False

# Check if "churn" column exists and contains only 0 or 1
if "churn" in df.columns:
    validation_results["churn_exists"] = True
    validation_results["churn_values_valid"] = df["churn"].dropna().isin([0, 1]).all()
else:
    validation_results["churn_exists"] = False
    validation_results["churn_values_valid"] = False

# Convert results to JSON
validation_report = json.dumps(validation_results, indent=4)

# Upload validation report to S3
s3.put_object(
    Bucket=s3_bucket,
    Key=s3_output_key,
    Body=validation_report,
    ContentType="application/json"
)

print("✅ Data validation complete. Report uploaded to S3:", s3_output_key)

