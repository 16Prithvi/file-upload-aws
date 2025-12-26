# AWS Serverless File Processing Pipeline

## 📌 Overview
This project implements an **event-driven, serverless backend** designed to automate file processing. When a file is uploaded to an Amazon S3 bucket, the system instantly triggers a validation and metadata extraction workflow, storing the results in Amazon DynamoDB.

The architecture adheres to core cloud-native principles—**scalability, least-privilege security, and cost-efficiency**—by operating entirely within the AWS Free Tier.

---

## 🏗 System Architecture

The pipeline follows a decoupled, event-driven flow as illustrated below:

1. **Trigger:** A user or system uploads a file to the **Amazon S3** bucket.
2. **Event:** S3 publishes an "Object Creation Event," which triggers **AWS Lambda**.
3. **Compute:** The Lambda function executes the logic to validate the file and extract metadata.
4. **Storage:** Processed metadata is persisted into an **Amazon DynamoDB** table.
5. **Observability:** Lambda streams execution logs and errors to **Amazon CloudWatch** for monitoring.

<img width="866" height="543" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/38ba1b3b-480f-42d7-a1dd-ccf44d1d2b7e" />

---

## 🛠 Tech Stack
* **Storage:** Amazon S3 (Simple Storage Service)
* **Compute:** AWS Lambda (Python 3.9 / Boto3 SDK)
* **Database:** Amazon DynamoDB (NoSQL)
* **Security:** AWS IAM (Identity and Access Management)
* **Monitoring:** Amazon CloudWatch Logs

---

## 🚀 Key Features
* **Event-Driven:** Zero-latency processing triggered immediately upon file upload.
* **Optimized Storage:** Efficient DynamoDB schema design for fast metadata retrieval.
* **Security-First:** Implements least-privilege access using granular IAM policies.
* **Validation Logic:** Automated checks for file types and constraints prior to storage.
* **Full Observability:** Real-time debugging and historical execution tracking via CloudWatch.

---

## 🔧 Implementation Details

### 1. Amazon S3 Bucket (Source)
A dedicated S3 bucket, shown below as `file-upload-bucket-nep-1`, serves as the landing zone for raw files. It is configured to send an event notification on `s3:ObjectCreated:*` actions to invoke the backend Lambda function.

<img width="866" height="543" alt="S3 Bucket Overview" src="https://github.com/user-attachments/assets/a5bf1be4-84d2-40b9-8c8e-e655acbdd291" />

### 2. IAM Role & Security
To ensure secure execution, a custom IAM Role was created for the Lambda function with strictly scoped permissions:
* `s3:GetObject`: Read access limited strictly to the source S3 bucket.
* `dynamodb:PutItem`: Write access limited to the metadata DynamoDB table.
* `logs:*`: Permissions to write execution events to CloudWatch logs.

### 3. AWS Lambda Function (Processor)
The core logic is handled by a Python 3.9 Lambda function shown below. The code initializes Boto3 clients for S3 and DynamoDB, parses the incoming event to retrieve the bucket name and file key, and passes them to a processing handler.

<img width="866" height="543" alt="Lambda Function Console" src="https://github.com/user-attachments/assets/df623746-a04e-47eb-9abc-af692cf3f8c5" />

### 4. Amazon DynamoDB (Metadata Storage)
Extracted metadata is stored based on the schema defined below. The screenshot confirms that files uploaded to S3 (like `sample.pdf` and `test.txt`) have been successfully processed and their details populated in the table with a status of `PROCESSED`.

**Table Schema:**
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `documentId` | String (PK) | Unique identifier (UUID) |
| `fileName` | String | Original name of the file |
| `fileType` | String | MIME type (e.g., application/pdf) |
| `fileSize` | Number | Size in bytes |
| `status` | String | Processing state (SUCCESS/FAILED) |
| `uploadedAt` | String | ISO 8601 timestamp |

<img width="866" height="543" alt="DynamoDB Table Items" src="https://github.com/user-attachments/assets/c9684ef8-7863-4c5e-8b83-4399584c0a5e" />

---

## 📊 Testing & Validation
The system was validated through various scenarios. The CloudWatch logs below provide proof of a successful execution flow.

1. **Success Path:** Uploaded `sample.pdf`. The logs confirm the function triggered correctly and outputted specific metadata: `"File sample.pdf processed with status PROCESSED, words=446"`.
2. **Error Handling:** Verified that invalid files (e.g., exceeding size limits) are caught by validation logic and logged as errors without corrupting the database.
3. **Security:** Verified that the Lambda role cannot access resources outside its defined scope.

<img width="666" height="443" alt="cloudwatch-img" src="https://github.com/user-attachments/assets/b4091f85-6557-40ac-b7d1-9ccd5c032933" />

---

## 💡 Key Learnings
* **Event-Driven Architectures:** Designing systems that react asynchronously to state changes rather than polling.
* **Cloud Security Posture:** The critical importance of defining granular IAM policies to minimize the attack surface.
* **NoSQL Data Modeling:** Designing efficient, single-table schemas in DynamoDB for operational workloads.
* **Serverless Operations:** Managing the lifecycle and monitoring of Functions-as-a-Service (FaaS).

---

## 🛠 Future Roadmap
* **AI/ML Integration:** Incorporate **Amazon Textract** for deep document OCR and data extraction.
* **Enhanced Security:** Integrate antivirus scanning on S3 uploads prior to triggering the processing workflow.
* **User Notifications:** Use **Amazon SNS** to send email or SMS alerts upon successful processing or failures.
* **Frontend Application:** Develop a modern **Next.js** web interface for users to upload files and visualize processed metadata.
