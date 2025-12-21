data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/trigger_glue.py"
  output_path = "${path.module}/../lambda/trigger_glue.zip"
}

resource "aws_lambda_function" "trigger" {
  function_name = "trigger-glue-job-${local.suffix}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "trigger_glue.lambda_handler"
  runtime       = "python3.10"
  filename      = data.archive_file.lambda_zip.output_path

  environment {
    variables = {
      GLUE_JOB_NAME = aws_glue_job.etl.name
    }
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3-${local.suffix}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.trigger.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw.arn
}

resource "aws_s3_bucket_notification" "raw_notify" {
  bucket = aws_s3_bucket.raw.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.trigger.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "sales/"
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_permission.allow_s3]
}

output "lambda_name" {
  value = aws_lambda_function.trigger.function_name
}
