provider "aws" {
  region = var.aws_region
}

module "api_gateway" {
  source = "./modules/api_gateway"

  api_name = var.api_name
  domain_name = module.route53.domain_name
}

module "route53" {
  source = "./modules/route53"

  domain_name = var.domain_name
  fargate_service_name = module.fargate.service_name
  fargate_service_arn = module.fargate.service_arn
}

module "fargate" {
  source = "./modules/fargate"

  app_name = var.app_name
  app_image = module.ecr.repository_url
  app_port = var.app_port
  vpc_id = var.vpc_id
  subnet_ids = var.subnet_ids
}

module "lambda" {
  source = "./modules/lambda"

  dynamodb_table_name = module.dynamodb.table_name
  ses_email_address = var.ses_email_address
}

module "dynamodb" {
  source = "./modules/dynamodb"

  table_name = var.dynamodb_table_name
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = var.ecr_repository_name
}

module "iam" {
  source = "./modules/iam"

  app_name = var.app_name
}