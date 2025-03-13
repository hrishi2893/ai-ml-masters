from flask import Flask, request, jsonify
import boto3
import pandas as pd
from io import StringIO

# ✅ Flask App Setup
app = Flask(__name__)

# ✅ S3 Configuration
s3_bucket = "dmmlassignment"
s3_transformed_data_key = "dmmlassignment-customer-churn/transformed_customer_churn_data.csv"

# ✅ Initialize S3 client
s3 = boto3.client("s3")

def get_features(feature_names):
    """Retrieve selected features from the transformed dataset in S3."""
    response = s3.get_object(Bucket=s3_bucket, Key=s3_transformed_data_key)
    df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

    # ✅ Ensure requested features exist
    missing_features = [f for f in feature_names if f not in df.columns]
    if missing_features:
        return {"error": f"Missing features: {missing_features}"}, 400

    return df[feature_names].to_dict(orient="records")

# ✅ API Endpoint for Feature Retrieval
@app.route("/features", methods=["GET"])
def retrieve_features():
    requested_features = request.args.getlist("feature")
    if not requested_features:
        return jsonify({"error": "No features requested"}), 400

    data, status = get_features(requested_features)
    return jsonify(data), status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

