variable "domain_name" {
  description = "Domain name for Route53"
  type        = string
}

variable "fargate_service_name" {
  description = "Name of the Fargate service"
  type        = string
}

variable "fargate_service_arn" {
  description = "ARN of the Fargate service"
  type        = string
}