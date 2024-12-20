data "aws_service_discovery_dns_namespace" "dns_namespace" {
  name = var.fargate_service_name
  type = "DNS_PRIVATE"
}

resource "aws_route53_zone" "otp_domain" {
  name = var.domain_name
}

resource "aws_service_discovery_service" "otp_app" {
  name = var.fargate_service_name

  dns_config {
    namespace_id = data.aws_service_discovery_dns_namespace.dns_namespace.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

resource "aws_route53_record" "otp_app" {
  zone_id = aws_route53_zone.otp_domain.zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_service_discovery_service.otp_app.name
    zone_id                = data.aws_service_discovery_dns_namespace.dns_namespace.id
    evaluate_target_health = true
  }
}