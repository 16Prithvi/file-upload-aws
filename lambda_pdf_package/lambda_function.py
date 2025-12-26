import json
import boto3
import os
import uuid
import io
from datetime import datetime
import PyPDF2

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

ALLOWED_EXTENSIONS = os.environ["ALLOWED_EXTENSIONS"].split(",")
MAX_FILE_SIZE_MB = int(os.environ["MAX_FILE_SIZE_MB"])


def extract_text_from_pdf(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    pdf_bytes = response["Body"].read()

    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "

    return text.strip()


def lambda_handler(event, context):
    try:
        record = event["Records"][0]
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]
        file_size = record["s3"]["object"]["size"]

        extension = object_key.split(".")[-1].lower()
        status = "PROCESSED"
        extracted_text = ""
        word_count = 0

        if extension not in ALLOWED_EXTENSIONS:
            status = "FAILED"

        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            status = "FAILED"

        if extension == "pdf" and status == "PROCESSED":
            extracted_text = extract_text_from_pdf(bucket_name, object_key)
            word_count = len(extracted_text.split())

        item = {
            "documentId": str(uuid.uuid4()),
            "fileName": object_key,
            "fileType": extension,
            "fileSize": file_size,
            "status": status,
            "uploadedAt": datetime.utcnow().isoformat(),
            "wordCount": word_count,
            "textPreview": extracted_text[:500]
        }

        table.put_item(Item=item)

        print(f"File {object_key} processed with status {status}, words={word_count}")

        return {
            "statusCode": 200,
            "body": json.dumps("Success")
        }

    except Exception as e:
        print("Error:", str(e))
        raise e
