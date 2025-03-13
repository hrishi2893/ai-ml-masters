import os
import logging
import boto3
import pandas as pd
import psycopg2
import kagglehub
from botocore.exceptions import NoCredentialsError, BotoCoreError

# Configure logging
logging.basicConfig(
    filename="ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 Data Ingestion Script Started.")

# Kaggle dataset details
KAGGLE_DATASET = "blastchar/telco-customer-churn"
LOCAL_CSV_FILE = "customer_churn_data.csv"

# AWS S3 details
S3_BUCKET_NAME = "dmmlassignment"
S3_OBJECT_KEY = "dmmlassignment-customer-churn/" + LOCAL_CSV_FILE

# AWS RDS PostgreSQL details
DB_HOST = "customer-churn.cluster-c5omwscqix0n.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = ""

# Download dataset from Kaggle
try:
    logging.info("📥 Downloading dataset from Kaggle...")
    dataset_path = kagglehub.dataset_download(KAGGLE_DATASET)
    df = pd.read_csv(os.path.join(dataset_path, "WA_Fn-UseC_-Telco-Customer-Churn.csv"))
    df.to_csv(LOCAL_CSV_FILE, index=False)
    logging.info(f"✅ Dataset downloaded successfully. Shape: {df.shape}")
except Exception as e:
    logging.error(f"❌ Error downloading dataset: {str(e)}")
    exit(1)

# Upload CSV to S3
try:
    logging.info("⬆️ Uploading data to S3...")
    s3_client = boto3.client("s3")
    s3_client.upload_file(LOCAL_CSV_FILE, S3_BUCKET_NAME, S3_OBJECT_KEY)
    logging.info(f"✅ Successfully uploaded {LOCAL_CSV_FILE} to S3 bucket {S3_BUCKET_NAME}")
except (NoCredentialsError, BotoCoreError) as e:
    logging.error(f"❌ AWS S3 upload error: {str(e)}")
    exit(1)

# Connect to PostgreSQL RDS
try:
    logging.info("🔗 Connecting to PostgreSQL RDS...")
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    logging.info("✅ Successfully connected to RDS.")
except Exception as e:
    logging.error(f"❌ Error connecting to RDS: {str(e)}")
    exit(1)

# Create table in RDS (if not exists)
try:
    logging.info("📌 Creating table if it doesn't exist...")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS customer_churn (
        customerID VARCHAR(50) PRIMARY KEY,
        gender VARCHAR(10),
        SeniorCitizen INT,
        Partner VARCHAR(10),
        Dependents VARCHAR(10),
        tenure INT,
        PhoneService VARCHAR(10),
        MultipleLines VARCHAR(20),
        InternetService VARCHAR(20),
        OnlineSecurity VARCHAR(20),
        OnlineBackup VARCHAR(20),
        DeviceProtection VARCHAR(20),
        TechSupport VARCHAR(20),
        StreamingTV VARCHAR(20),
        StreamingMovies VARCHAR(20),
        Contract VARCHAR(20),
        PaperlessBilling VARCHAR(10),
        PaymentMethod VARCHAR(50),
        MonthlyCharges FLOAT,
        TotalCharges VARCHAR(20),
        Churn VARCHAR(10)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    logging.info("✅ Table checked/created successfully.")
except Exception as e:
    logging.error(f"❌ Error creating table: {str(e)}")
    exit(1)

# Insert data into PostgreSQL
try:
    logging.info("📤 Inserting data into PostgreSQL RDS...")
    
    for _, row in df.iterrows():
        insert_query = """
        INSERT INTO customer_churn VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customerID) DO NOTHING;
        """
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    logging.info(f"✅ Successfully inserted {df.shape[0]} records into PostgreSQL.")
except Exception as e:
    logging.error(f"❌ Error inserting data: {str(e)}")
    exit(1)

# Close database connection
cursor.close()
conn.close()
logging.info("✅ Database connection closed.")

logging.info("🎯 Data Ingestion Script Completed Successfully.")

