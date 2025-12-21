resource "aws_s3_bucket" "raw" {
  bucket = "etl-raw-${local.suffix}"
}

resource "aws_s3_bucket" "processed" {
  bucket = "etl-processed-${local.suffix}"
}

resource "aws_s3_bucket" "scripts" {
  bucket = "etl-scripts-${local.suffix}"
}

output "raw_bucket" {
  value = aws_s3_bucket.raw.bucket
}

output "processed_bucket" {
  value = aws_s3_bucket.processed.bucket
}

output "scripts_bucket" {
  value = aws_s3_bucket.scripts.bucket
}
