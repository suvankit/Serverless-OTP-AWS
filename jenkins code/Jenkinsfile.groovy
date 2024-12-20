pipeline{

	agent {label 'winsalve1'}

	environment {
		DOCKERHUB_CREDENTIALS=credentials('dockerhub')
	}

	stages {
	    
	    stage('gitclone') {

			steps {
				git 'https://github.com/shazforiot/nodeapp_test.git'
			}
		}

		stage('Build') {

			steps {
				sh 'docker build -t thetips4you/nodeapp_test:latest .'
			}
		}

		stage('Login') {

			steps {
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
			}
		}

		stage('Push') {

			steps {
				sh 'docker push thetips4you/nodeapp_test:latest'
			}
		}
	}

	post {
		always {
			sh 'docker logout'
		}
	}

}




pipeline {
    agent any

    environment {
        ECR_REGISTRY = '<your-ecr-registry-uri>'
        APP_NAME = 'otp-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: '<your-git-repo-url>'
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.build("${ECR_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}", '.')
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry("${ECR_REGISTRY}", 'ecr:us-east-1:<your-aws-account-id>') {
                        docker.image("${ECR_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Update Lambda function code with the new image URI
                    // Deploy API Gateway changes
                }
            }
        }
    }
}

# Fetch available subnets and AZs
data "aws_subnets" "subnets" {
  vpc_id = var.vpc_id
}

data "aws_availability_zones" "available" {}

# Create a list of subnet/AZ pairs sorted by available IP addresses
locals {
  subnet_az_pairs = { for idx, subnet in data.aws_subnets.subnets.ids :
    subnet => {
      az  = data.aws_availability_zones.available.names[idx % length(data.aws_availability_zones.available.names)]
      ips = data.aws_subnet.subnet[subnet].available_ip_address_count
    }
  }

  sorted_subnet_az_pairs = sort([for pair in local.subnet_az_pairs : pair], reverse(true), [for pair in local.subnet_az_pairs : pair.1.ips])
}

# Allocate instances dynamically
resource "aws_instance" "example" {
  count = var.instance_count

  ami           = var.ami
  instance_type = var.instance_type

  # Allocate instances to the subnet with the highest available IPs
  subnet_id              = local.sorted_subnet_az_pairs[count.index % length(local.sorted_subnet_az_pairs)].0
  availability_zone      = local.sorted_subnet_az_pairs[count.index % length(local.sorted_subnet_az_pairs)].1.az
  associate_public_ip_address = true

  # Other instance configurations...
}