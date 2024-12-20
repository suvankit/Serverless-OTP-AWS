variable "app_name" {
  description = "Name of the application"
  type        = string
}

variable "app_image" {
  description = "Docker image for the application"
  type        = string
}

variable "app_port" {
  description = "Port on which the application listens"
  type        = number
}

variable "vpc_id" {
  description = "VPC ID to deploy the Fargate service"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs to deploy the Fargate service"
  type        = list(string)
}