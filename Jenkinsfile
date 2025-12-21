pipeline {
  agent any

  environment {
    DB_HOST = 'etl-rds-etldb-fhd3nychlg6p.cijyq4iwk497.us-east-1.rds.amazonaws.com'
    DB_PORT = '5432'
    DB_NAME = 'etldb'
    DB_USER = 'etluser'
    DB_PASS = 'StrongPassword123!'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup venv + deps') {
      steps {
        sh '''
          set -e
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip
          pip install psycopg2-binary openpyxl
        '''
      }
    }

    stage('Create Tables (reset schema)') {
      steps {
        sh '''
          set -e

          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -c "DROP TABLE IF EXISTS sales;"

          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -c "CREATE TABLE sales (
                  order_id INT,
                  customer_id INT,
                  amount NUMERIC(10,2),
                  order_date DATE
                );"

          # Debug: show schema
          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -c "\\d sales"
        '''
      }
    }

    stage('Load Data from CSV') {
      steps {
        sh '''
          set -e

          # Clear old data so reruns don't duplicate
          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -c "TRUNCATE TABLE sales;"

          # Load CSV from the repo workspace into Postgres
          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -c "\\copy sales(order_id,customer_id,amount,order_date) FROM 'sample_data/sales.csv' WITH (FORMAT csv, HEADER true, NULL '')"

          # Debug: confirm row count
          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -c "SELECT COUNT(*) AS sales_rows FROM sales;"
        '''
      }
    }

    stage('Generate Excel Report') {
      steps {
        sh '''
          set -e
          . .venv/bin/activate

          # Ensure reports folder exists
          mkdir -p reports

          python reports/generate_sales_report.py

          echo "Workspace files:"
          ls -la
          echo "Reports folder:"
          ls -la reports
        '''
      }
    }
  }

  post {
    success {
      archiveArtifacts artifacts: 'reports/*.xlsx', fingerprint: true
    }
  }
}
