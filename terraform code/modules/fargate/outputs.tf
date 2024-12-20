output "service_name" {
  description = "Name of the Fargate service"
  value       = aws_ecs_service.otp_service.name
}

output "service_arn" {
  description = "ARN of the Fargate service"
  value       = aws_ecs_service.otp_service.id
}