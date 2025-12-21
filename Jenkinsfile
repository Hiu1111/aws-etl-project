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
      steps { checkout scm }
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
          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "DROP TABLE IF EXISTS sales;"
          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "DROP TABLE IF EXISTS sales_staging;"

          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
            CREATE TABLE sales (
              order_id INT,
              customer_id INT,
              amount NUMERIC(10,2),
              tax NUMERIC(10,2),
              order_date DATE
            );
          "

          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
            CREATE TABLE sales_staging (
              order_id INT,
              customer_id INT,
              amount NUMERIC(10,2),
              order_date DATE
            );
          "
        '''
      }
    }

    stage('Load Data from CSV (compute tax)') {
      steps {
        sh '''
          set -e
          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE sales;"
          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE sales_staging;"

          wc -l sample_data/sales.csv

          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME \
            -c "\\copy sales_staging(order_id,customer_id,amount,order_date) FROM 'sample_data/sales.csv' WITH (FORMAT csv, HEADER true, NULL '')"

          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
            INSERT INTO sales(order_id, customer_id, amount, tax, order_date)
            SELECT
              order_id,
              customer_id,
              amount,
              ROUND(COALESCE(amount,0) * 0.10, 2) AS tax,
              order_date
            FROM sales_staging;
          "

          PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) AS sales_rows FROM sales;"
        '''
      }
    }

    stage('Generate Excel Report') {
      steps {
        sh '''
          set -e
          . .venv/bin/activate
          mkdir -p reports
          python reports/generate_sales_report.py

          # Move the output into reports so Jenkins can archive it
          mv -f sales_report.xlsx reports/

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
