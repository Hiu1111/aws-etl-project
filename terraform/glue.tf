resource "aws_glue_job" "etl" {
  name     = "etl-glue-job-${local.suffix}"
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://${aws_s3_bucket.scripts.bucket}/etl_job.py"
  }

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2

  default_arguments = {
    "--RAW_BUCKET"       = aws_s3_bucket.raw.bucket
    "--PROCESSED_BUCKET" = aws_s3_bucket.processed.bucket
  }
}

output "glue_job_name" {
  value = aws_glue_job.etl.name
}
