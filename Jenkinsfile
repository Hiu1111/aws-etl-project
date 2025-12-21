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
    stage('Install Dependencies') {
      steps {
        sh 'python3 -m pip install --user psycopg2-binary openpyxl'
      }
    }

    stage('Create Tables') {
      steps {
        sh '''
          PGPASSWORD=$DB_PASS psql \
            -h $DB_HOST -p $DB_PORT \
            -U $DB_USER -d $DB_NAME \
            -f sql/001_create_sales_table.sql
        '''
      }
    }

    stage('Generate Excel Report') {
      steps {
        sh 'python3 reports/generate_sales_report.py'
      }
    }
  }

  post {
    success {
      archiveArtifacts artifacts: 'reports/*.xlsx', fingerprint: true
    }
  }
}
