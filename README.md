# AWS Serverless File Processing Pipeline

## 📌 Overview
This project demonstrates an **event-driven, serverless backend** designed to automate file processing. When a file is uploaded to an Amazon S3 bucket, the system automatically triggers a validation and metadata extraction workflow, storing the results in Amazon DynamoDB. 

The architecture demonstrates core cloud-native principles: **scalability, least-privilege security, and cost-efficiency** by staying entirely within the AWS Free Tier.

---

## 🏗 System Architecture

The pipeline follows a decoupled, event-driven flow:
1. **Trigger:** A user or system uploads a file to **Amazon S3**.
2. **Event:** S3 sends a notification to **AWS Lambda**.
3. **Compute:** The Lambda function processes the file, validates its type/size, and extracts metadata.
4. **Storage:** Extracted data is persisted in **Amazon DynamoDB**.
5. **Observability:** All execution steps and errors are tracked via **Amazon CloudWatch**.



---

## 🛠 Tech Stack
* **Storage:** Amazon S3 (Simple Storage Service)
* **Compute:** AWS Lambda (Python / Boto3)
* **Database:** Amazon DynamoDB (NoSQL)
* **Security:** AWS IAM (Identity and Access Management)
* **Monitoring:** Amazon CloudWatch

---

## 🚀 Key Features
* **Automated Triggers:** Zero-latency processing upon file upload.
* **Schema Design:** Optimized DynamoDB table for fast metadata retrieval.
* **Security-First:** Custom IAM policies ensuring the Lambda function follows the Principle of Least Privilege.
* **Validation Logic:** Automated checks for file constraints.
* **Comprehensive Logging:** Real-time debugging and execution history through CloudWatch.

---

## 🔧 Implementation Details

### 1. Amazon S3 Configuration
A dedicated S3 bucket acts as the landing zone for raw files. 
* **Event Notification:** Configured to trigger on `s3:ObjectCreated:*` events to invoke the Lambda function.

> **[Insert Screenshot: S3 Bucket configuration and event notification settings]**

### 2. IAM Role & Security
To ensure a secure environment, I created a custom IAM Execution Role with the following policy actions:
* `s3:GetObject` (Limited to the source bucket)
* `dynamodb:PutItem` (Limited to the metadata table)
* `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

> **[Insert Screenshot: IAM Policy JSON or Role permissions summary]**

### 3. AWS Lambda Logic
The core processing engine. The function is responsible for:
* Parsing the S3 event object.
* Extracting metadata (File name, size, extension, upload time).
* Validating requirements before writing to the database.

### 4. DynamoDB Schema
The metadata is stored using the following schema:
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `documentId` | String (PK) | Unique identifier |
| `fileName` | String | Original name of the uploaded file |
| `fileType` | String | MIME type (e.g., image/jpeg) |
| `fileSize` | Number | Size in bytes |
| `status` | String | Processing state (SUCCESS/FAILED) |
| `uploadedAt` | String | ISO 8601 timestamp |

> **[Insert Screenshot: DynamoDB Table view showing successfully processed items]**

---

## 📊 Testing & Validation
To validate the system, I performed the following tests:
1.  **Success Path:** Uploaded a valid file; verified the record appeared in DynamoDB and logs showed "200 OK".
2.  **Error Handling:** Uploaded a file exceeding size limits; verified that CloudWatch captured the validation error.
3.  **Permissions Test:** Verified IAM blocked unauthorized service requests.

> **[Insert Screenshot: CloudWatch Log streams showing a successful execution flow]**

---

## 💡 Key Learnings
* **Event-Driven Design:** Understanding how to build systems that "react" to data events.
* **Cloud Security:** Implementation of granular IAM policies to reduce the attack surface.
* **NoSQL Modeling:** Designing efficient schemas for high-speed metadata storage.
* **Serverless Lifecycle:** Managing code execution without the overhead of server maintenance.

---

## 🛠 Future Roadmap
* **AI Integration:** Use **Amazon Textract** to perform OCR on uploaded documents.
* **Security Scanning:** Integrate malware scanning before processing.
* **Notifications:** Add **Amazon SNS** to send alerts upon successful processing.
* **Frontend Interface:** Build a **Next.js** dashboard for visualization.

---