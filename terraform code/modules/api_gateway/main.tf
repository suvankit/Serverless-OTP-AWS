resource "aws_api_gateway_rest_api" "otp_api" {
  name = var.api_name
}

resource "aws_api_gateway_resource" "proxy_root" {
  rest_api_id = aws_api_gateway_rest_api.otp_api.id
  parent_id   = aws_api_gateway_rest_api.otp_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy_root" {
  rest_api_id   = aws_api_gateway_rest_api.otp_api.id
  resource_id   = aws_api_gateway_resource.proxy_root.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "fargate_integration" {
  rest_api_id             = aws_api_gateway_rest_api.otp_api.id
  resource_id             = aws_api_gateway_resource.proxy_root.id
  http_method             = aws_api_gateway_method.proxy_root.http_method
  integration_http_method = "POST"
  type                    = "HTTP_PROXY"
  uri                     = "http://${var.domain_name}/{proxy}"
}

resource "aws_api_gateway_deployment" "otp_api_deployment" {
  depends_on = [
    aws_api_gateway_integration.fargate_integration
  ]
  rest_api_id = aws_api_gateway_rest_api.otp_api.id
  stage_name  = "prod"
}