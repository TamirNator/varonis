module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.6.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-west-1a", "us-west-1b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]

  tags = {
    Terraform = "true"
  }
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-eks-cluster"
  cluster_version = "1.21"
  subnets         = module.vpc.public_subnets
  vpc_id          = module.vpc.vpc_id

  node_groups = {
    eks_nodes = {
      desired_capacity = 1
      max_capacity     = 1
      min_capacity     = 1

      instance_type = "t3.medium"
    }
  }

  tags = {
    Terraform = "true"
  }
}