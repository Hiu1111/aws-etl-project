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

    stage('Create Tables') {
      steps {
        sh '''
          set -e
          . .venv/bin/activate
          ls -la sql
          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -f sql/001_create_sales_table.sql
        '''
      }
    }

    stage('Generate Excel Report') {
      steps {
        sh '''
          set -e
          . .venv/bin/activate
          python reports/generate_sales_report.py
          ls -la reports
        '''
      }
    }
  }

  post {
    success {
      archiveArtifacts artifacts: 'sales_report.xlsx', fingerprint: true
    }
  }
}
