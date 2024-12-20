variable "aws_region" {
  description = "AWS region to create resources"
  default     = "us-east-1"
}

variable "api_name" {
  description = "Name of the API Gateway"
  default     = "otp-api"
}

variable "domain_name" {
  description = "Domain name for Route53"
  default     = "example.com"
}

variable "app_name" {
  description = "Name of the application"
  default     = "otp-app"
}

variable "app_port" {
  description = "Port on which the application listens"
  default     = 8000
}

variable "vpc_id" {
  description = "VPC ID to deploy the Fargate service"
}

variable "subnet_ids" {
  description = "Subnet IDs to deploy the Fargate service"
  type        = list(string)
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  default     = "otp-table"
}

variable "ses_email_address" {
  description = "Email address to send OTPs from"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  default     = "otp-app"
}