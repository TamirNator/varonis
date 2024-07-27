#Create secret for postgresql Helm chart on AWS secrets Manager
aws secretsmanager create-secret --name postgresql-password --secret-string '{"password":"mypassword"}'
