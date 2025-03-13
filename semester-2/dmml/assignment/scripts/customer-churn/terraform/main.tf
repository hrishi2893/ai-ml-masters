provider "aws" {
  region = "us-east-1"  # Change as needed
}

# ✅ Create S3 Bucket
resource "aws_s3_bucket" "dmmlassignment" {
  bucket = "dmmlassignment"
  acl    = "private"  # Adjust ACL as needed
}

# ✅ Create EC2 Instance
resource "aws_instance" "customer_churn" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Change to your region's AMI
  instance_type          = "t2.medium"
  key_name               = "your-key"  # Ensure your key exists
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  tags = {
    Name = "customer-churn"
  }
}

# ✅ Security Group for EC2
resource "aws_security_group" "ec2_sg" {
  name        = "customer_churn_sg"
  description = "Allow SSH and DB Access"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restrict in production
  }
  
  ingress {
    from_port   = 3306  # Change for Postgres
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ✅ Create Aurora Database
resource "aws_rds_cluster" "customer_churn" {
  cluster_identifier      = "customer-churn"
  engine                 = "aurora-mysql"
  engine_version         = "8.0.mysql_aurora.3.04.0"
  master_username        = "admin"
  master_password        = ""  # Change for security
  skip_final_snapshot    = true
}

resource "aws_rds_cluster_instance" "customer_churn_instance" {
  cluster_identifier = aws_rds_cluster.customer_churn.id
  instance_class     = "db.t3.medium"
  engine            = aws_rds_cluster.customer_churn.engine
}

output "ec2_public_ip" {
  value = aws_instance.customer_churn.public_ip
}

