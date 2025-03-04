# **Customer Churn Prediction Pipeline Design**

## **1. Business Problem**
Customer churn occurs when an existing customer stops using a company’s services or purchasing its products. High churn rates lead to revenue loss and increased customer acquisition costs. This project aims to build an automated data pipeline that processes customer data and predicts churn using machine learning.

## **2. Key Business Objectives**
- Reduce customer churn by identifying at-risk customers early.
- Improve customer retention strategies by providing actionable insights.
- Automate data ingestion, transformation, and model deployment.
- Ensure scalability and efficiency in handling large volumes of customer data.

## **3. Key Data Sources and Attributes**

| Data Source               | Attributes                                       |
|---------------------------|------------------------------------------------|
| **Web Logs**              | Clickstream data, session duration, pages visited, time spent |
| **Transactional Data**    | Purchase history, subscription renewals, payment failures |
| **Customer Support Data** | Complaint logs, chat interactions, resolution time |
| **Third-Party APIs**      | Customer sentiment, credit scores, social media engagement |

## **4. Expected Pipeline Outputs** TODO
- **Clean datasets** for **Exploratory Data Analysis (EDA)**
- **Transformed features** ready for machine learning training
- **Deployable model** for real-time churn prediction

## **5. Measurable Evaluation Metrics**
- **Accuracy & Precision** – Model’s ability to correctly classify churners and non-churners.
- **Recall (Sensitivity)** – Ability to detect actual churners.
- **F1-score** – Balance between precision and recall.
- **AUC-ROC Score** – Model’s ability to distinguish between churners and non-churners.

