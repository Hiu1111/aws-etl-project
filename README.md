# 🛠️ AWS ETL Data Pipeline

An automated end-to-end ETL pipeline that ingests raw sales data, transforms it in the cloud, and loads it into a PostgreSQL database — with CI/CD orchestration and automated Excel reporting.

---

## ⚙️ Tech Stack

| Layer | Tools |
|---|---|
| Ingestion | Amazon S3 |
| Transformation | AWS Glue, Python |
| Loading | PostgreSQL on Amazon RDS |
| Orchestration | Jenkins CI/CD, AWS Lambda |
| Infrastructure | Terraform, CloudFormation |
| Reporting | Python, OpenPyExcel |

---

## 🔄 Pipeline Flow

```
S3 (Raw CSV) → AWS Glue (Transform) → RDS PostgreSQL (Load) → Excel Reports
                                ↑
                         Jenkins CI/CD
```

---

## 📁 Project Structure

```
aws-etl-project/
├── cloudformation/    # AWS CloudFormation templates
├── glue/              # Glue ETL transformation scripts
├── lambda/            # Lambda trigger functions
├── reports/           # Generated Excel reports
├── sample_data/       # 500-row sample sales dataset
├── sql/               # Table creation SQL
├── terraform/         # Terraform IaC configs
├── Jenkinsfile        # CI/CD pipeline definition
└── requirements.txt   # Python dependencies
```

---

## 🚀 Key Features

- **Automated ETL** — ingests CSV sales data from S3, computes derived fields (e.g. tax), and loads into PostgreSQL on RDS
- **CI/CD Pipeline** — Jenkins orchestrates repeatable data refreshes and report generation on every run
- **Infrastructure as Code** — all AWS resources (RDS, S3, IAM, Glue, Lambda) provisioned via Terraform and CloudFormation
- **Automated Reporting** — Excel reports generated from transformed records using Python and OpenPyExcel

---

## 🛠️ Setup

```bash
# 1. Provision infrastructure
cd terraform/ && terraform init && terraform apply

# 2. Install dependencies
pip install -r requirements.txt

# 3. Upload sample data
aws s3 cp sample_data/ s3://<your-bucket>/input/ --recursive

# 4. Run the Glue job
aws glue start-job-run --job-name <your-glue-job-name>
```
