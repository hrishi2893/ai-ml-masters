import boto3
import pandas as pd
import mlflow
import mlflow.sklearn
import pickle
from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ✅ S3 Configuration
s3_bucket = "dmmlassignment"
s3_transformed_data_key = "dmmlassignment-customer-churn/transformed_customer_churn_data.csv"
model_save_path = "dmmlassignment-customer-churn/churn_model.pkl"

# ✅ Initialize S3 client
s3 = boto3.client("s3")

# ✅ Load transformed dataset from S3
response = s3.get_object(Bucket=s3_bucket, Key=s3_transformed_data_key)
df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

# ✅ Feature selection
features = ["customer_tenure_days", "avg_transaction_value"]
target = "Churn"

X = df[features]
y = df[target].apply(lambda x: 1 if x == "Yes" else 0)  # Convert to binary

# ✅ Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train models
models = {
    "LogisticRegression": LogisticRegression(),
    "RandomForest": RandomForestClassifier(n_estimators=100)
}

best_model = None
best_f1 = 0
results = {}

mlflow.set_experiment("Customer Churn Prediction")

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # ✅ Evaluate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }

    # ✅ Log to MLflow
    with mlflow.start_run():
        mlflow.log_param("Model", name)
        mlflow.log_metric("Accuracy", accuracy)
        mlflow.log_metric("Precision", precision)
        mlflow.log_metric("Recall", recall)
        mlflow.log_metric("F1 Score", f1)
        mlflow.sklearn.log_model(model, name)

    # ✅ Select best model
    if f1 > best_f1:
        best_f1 = f1
        best_model = model

# ✅ Save the best model
model_buffer = pickle.dumps(best_model)
s3.put_object(Bucket=s3_bucket, Key=model_save_path, Body=model_buffer)

print("✅ Model training complete.")
print("🏆 Best Model:", best_model)
print("📊 Model Performance:", results)
print("📁 Model saved to S3:", f"s3://{s3_bucket}/{model_save_path}")

