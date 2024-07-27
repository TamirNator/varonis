provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

data "aws_secretsmanager_secret_version" "postgresql_password" {
  secret_id = "postgresql-password"
}

resource "helm_release" "postgresql" {
  name       = "my-postgresql"
  chart      = "/helm/postgresql"
  namespace  = "default"

  values = [
    <<EOF
auth:
  database: "requests_db"
  username: "myuser"
  password: ${jsondecode(data.aws_secretsmanager_secret_version.postgresql_password.secret_string)["password"]}
service:
  type: ClusterIP
primary:
  persistence:
    enabled: false
EOF
  ]
}