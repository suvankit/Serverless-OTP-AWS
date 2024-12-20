output "endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_api_gateway_deployment.otp_api_deployment.invoke_url
}