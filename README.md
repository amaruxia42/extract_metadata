🧬 Genomics England — AWS/Terraform/Python Test
Challenge Overview

This exercise demonstrates a serverless AWS solution for automatically sanitizing uploaded images by removing EXIF metadata. The system provisions two S3 buckets, an AWS Lambda function, and IAM users with scoped permissions, all defined using Terraform.
Requirements

    Image Processing

        Users upload .jpg images to S3 Bucket A.

        A Lambda function strips EXIF metadata and writes the cleaned image to S3 Bucket B, preserving the original object path.

    Access Control

        User A: Read/Write access to Bucket A.

        User B: Read‑only access to Bucket B.

📸 Solution Design

The solution leverages AWS Lambda for lightweight, event‑driven processing. Since EXIF metadata is typically small (1–50 KB, max ~64 KB), Lambda is well‑suited for this workload.

Workflow:

    A .jpg file is uploaded to Bucket A.

    An S3 event notification triggers the Lambda function.

    The Lambda function:

        Retrieves the image from Bucket A.

        Uses the Python exif library to detect and remove metadata.

        Writes the sanitized image to Bucket B, maintaining the same key.

    Clean images in Bucket B are then available for use on the website.

🎯 Objectives

    ✅ Automatically remove sensitive EXIF metadata (location, timestamps, device info).

    ✅ Separate raw and sanitized images into distinct buckets.

    ✅ Enforce least‑privilege access via IAM policies.

    ✅ Provision all resources with Infrastructure‑as‑Code (Terraform).

🔐 IAM & Access Control
User	Permissions
User A	Read/Write access to Bucket A
User B	Read‑only access to Bucket B

Lambda Execution Role:

    Read from Bucket A

    Write to Bucket B

    Publish logs to CloudWatch

🧰 Tech Stack
Technology	Purpose
AWS S3	Object storage for raw & clean images
AWS Lambda	Event‑driven EXIF removal
AWS IAM	Scoped access control
CloudWatch	Monitoring and logging
Terraform	Infrastructure‑as‑Code provisioning
Python 3.13	Lambda runtime
exif module	Metadata detection and removal
🚀 Deployment

    Provision Infrastructure
    bash
    terraform init
    terraform apply

    Package Lambda
    bash
    zip -r lambda_exif_cleaner.zip lambda_function.py

    Deploy Lambda Terraform references the ZIP file and uploads it to AWS.

🧪 Testing

    Upload a .jpg with EXIF metadata to Bucket A.

    Verify the corresponding object in Bucket B has no EXIF metadata.

    Check CloudWatch Logs for Lambda execution details.

🗂️ Project Structure
    Code
    ├── main.tf                  # Terraform configuration
    ├── provider.tf              # AWS provider definition
    ├── lambda_function.py       # Python logic for EXIF cleaning
    ├── lambda_exif_cleaner.zip  # Lambda deployment package
    ├── README.md                # Documentation

🔮 Future Enhancements

    Add bucket encryption and versioning for stronger security.

    Extend support to other image formats (e.g., PNG).

    Integrate CI/CD pipeline for Lambda updates.

    Add CloudWatch alarms for error monitoring.
