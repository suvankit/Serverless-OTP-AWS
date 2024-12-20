output "domain_name" {
  description = "Domain name for the application"
  value       = aws_route53_zone.otp_domain.name
}