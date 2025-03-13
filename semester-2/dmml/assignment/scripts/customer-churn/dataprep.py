import boto3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder

# AWS S3 Configuration
bucket_name = "dmmlassignment"
raw_file_key = "dmmlassignment-customer-churn/customer_churn_data.csv"  # Raw file path in S3
processed_file_key = "dmmlassignment-customer-churn/processed/cleaned_data.csv"  # Destination in S3

# Initialize S3 client
s3 = boto3.client("s3")

# Read CSV from S3
obj = s3.get_object(Bucket=bucket_name, Key=raw_file_key)
df = pd.read_csv(obj["Body"])

print("🔹 Raw Data Sample:\n", df.head())

# ----- Handle Missing Values -----
df.fillna(df.median(numeric_only=True), inplace=True)  # Fill missing numerics with median
df.fillna("Unknown", inplace=True)  # Fill missing categoricals with "Unknown"

# ----- Standardize Numerical Features -----
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# ----- Encode Categorical Variables -----
cat_cols = df.select_dtypes(include=["object"]).columns
encoder = LabelEncoder()
for col in cat_cols:
    df[col] = encoder.fit_transform(df[col])

# ----- EDA: Data Distribution -----
plt.figure(figsize=(10, 5))
sns.histplot(df[num_cols[0]], kde=True)  # Histogram of first numeric column
plt.title(f"Distribution of {num_cols[0]}")
plt.show()

plt.figure(figsize=(10, 5))
sns.boxplot(data=df[num_cols])
plt.title("Box Plot of Numeric Features")
plt.show()

# Save cleaned dataset locally (temporary storage)
cleaned_file = "/tmp/cleaned_data.csv"  
df.to_csv(cleaned_file, index=False)

# Upload cleaned file to S3
s3.upload_file(cleaned_file, bucket_name, processed_file_key)

print(f"✅ Cleaned data uploaded to S3: s3://{bucket_name}/{processed_file_key}")

