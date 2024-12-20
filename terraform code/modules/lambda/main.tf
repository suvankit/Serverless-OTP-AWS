data "archive_file" "generate_otp_lambda" {
  type        = "zip"
  source_file = "${path.module}/generate_otp.py"
  output_path = "${path.module}/