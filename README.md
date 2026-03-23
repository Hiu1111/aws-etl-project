AWS ETL Data Pipeline Project
An end-to-end automated ETL pipeline that ingests, transforms, and loads sales data into a PostgreSQL database on Amazon RDS, with CI/CD orchestration via Jenkins and automated Excel report generation.
Tech Stack
Python SQL AWS Glue AWS Lambda Amazon RDS Amazon S3 Jenkins Terraform CloudFormation
Architecture Overview
Raw CSV Data (S3)
      │
      ▼
AWS Glue (Transform + Compute Derived Fields)
      │
      ▼
AWS Lambda (Trigger / Orchestration)
      │
      ▼
PostgreSQL on Amazon RDS (Load)
      │
      ▼
Python + OpenPyExcel (Automated Excel Reports)
Project Structure
aws-etl-project/
├── cloudformation/     # CloudFormation templates for AWS resource provisioning
├── glue/               # AWS Glue ETL scripts (Python)
├── lambda/             # Lambda function handlers
├── reports/            # Generated Excel report outputs
├── sample_data/        # Sample 500-row sales dataset (CSV)
├── sql/                # Table creation and query SQL scripts
├── terraform/          # Terraform IaC for RDS, S3, IAM, Glue, Lambda
├── Jenkinsfile         # CI/CD pipeline definition
└── requirements.txt    # Python dependencies
Features

Automated ETL Pipeline — ingests raw CSV sales data from S3, applies transformations (e.g. tax computation), and loads clean records into PostgreSQL on RDS
CI/CD with Jenkins — Jenkinsfile orchestrates pipeline execution, enabling repeatable data refreshes and automated report generation on each run
AWS Glue Transformations — PySpark/Python Glue jobs compute derived fields and handle data cleaning during transformation
Infrastructure as Code — full cloud infrastructure provisioned with Terraform and CloudFormation, covering RDS, S3, IAM roles, Glue, and Lambda resources
Automated Reporting — Python scripts using OpenPyExcel generate formatted Excel reports directly from transformed database records
