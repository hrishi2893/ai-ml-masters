import pandas as pd
import pg8000

# Database connection parameters
DB_HOST = "customer-churn.cluster-c5omwscqix0n.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = ""

# CSV file path
csv_file_path = 's3://dmmlassignment/dmmlassignment-customer-churn/customer_churn_data.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Establish a connection to the PostgreSQL database
conn = pg8000.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Create the customer_churn table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS customer_churn (
    customer_id VARCHAR PRIMARY KEY,
    gender VARCHAR,
    senior_citizen BOOLEAN,
    partner BOOLEAN,
    dependents BOOLEAN,
    tenure INTEGER,
    phone_service BOOLEAN,
    multiple_lines BOOLEAN,
    internet_service VARCHAR,
    online_security BOOLEAN,
    online_backup BOOLEAN,
    device_protection BOOLEAN,
    tech_support BOOLEAN,
    streaming_tv BOOLEAN,
    streaming_movies BOOLEAN,
    contract VARCHAR,
    paperless_billing BOOLEAN,
    payment_method VARCHAR,
    monthly_charges NUMERIC,
    total_charges NUMERIC,
    churn BOOLEAN
);
'''
cursor.execute(create_table_query)
conn.commit()

# Insert DataFrame rows into the customer_churn table
insert_query = '''
INSERT INTO customer_churn (
    customer_id, gender, senior_citizen, partner, dependents, tenure,
    phone_service, multiple_lines, internet_service, online_security,
    online_backup, device_protection, tech_support, streaming_tv,
    streaming_movies, contract, paperless_billing, payment_method,
    monthly_charges, total_charges, churn
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
'''

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row['customerID'], row['gender'], row['SeniorCitizen'], row['Partner'],
        row['Dependents'], row['tenure'], row['PhoneService'], row['MultipleLines'],
        row['InternetService'], row['OnlineSecurity'], row['OnlineBackup'],
        row['DeviceProtection'], row['TechSupport'], row['StreamingTV'],
        row['StreamingMovies'], row['Contract'], row['PaperlessBilling'],
        row['PaymentMethod'], row['MonthlyCharges'], row['TotalCharges'],
        row['Churn']
    ))

conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data inserted successfully.")

