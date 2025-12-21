import json
import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    job_name = os.environ['GLUE_JOB_NAME']

    response = glue.start_job_run(JobName=job_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Started Glue job: {response['JobRunId']}")
    }
