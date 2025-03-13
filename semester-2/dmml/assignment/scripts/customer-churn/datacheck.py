import pandas as pd
import boto3
import io

# ✅ AWS S3 Configuration
s3_bucket = "dmmlassignment"
s3_key = "dmmlassignment-customer-churn/customer_churn_data.csv"  # Update the correct path

# ✅ Initialize S3 client
s3 = boto3.client("s3")

try:
    # ✅ Fetch CSV from S3
    response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    df = pd.read_csv(io.BytesIO(response["Body"].read()))

    # ✅ Print DataFrame columns
    print("\n📌 Columns in the DataFrame:")
    print(df.columns.tolist())

    # ✅ Normalize column names (convert to lowercase, remove spaces)
    normalized_columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    print("\n📌 Normalized column names (for reference):")
    print(normalized_columns)

    # ✅ Expected column names in the database
    expected_columns = ["customer_id", "churn", "tenure", "monthly_charges", "total_charges"]  # Modify as needed

    # ✅ Check for missing or extra columns
    missing_columns = [col for col in expected_columns if col not in normalized_columns]
    extra_columns = [col for col in normalized_columns if col not in expected_columns]

    # ✅ Print results
    if missing_columns:
        print(f"\n❌ Missing columns in the DataFrame: {missing_columns}")
    else:
        print("\n✅ All required columns are present!")

    if extra_columns:
        print(f"\n⚠️ Extra columns found in the DataFrame (not expected in the DB): {extra_columns}")

except Exception as e:
    print(f"\n❌ Error fetching file from S3: {e}")


