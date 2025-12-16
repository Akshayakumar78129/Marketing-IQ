# Terraform (Infrastructure as Code)

Azure infrastructure definitions.

## Structure

```
terraform/
├── production/              # Production environment
│   ├── main.tf
│   └── terraform.tfvars
├── modules/                 # Reusable modules
│   ├── synapse/
│   ├── storage/
│   └── container_apps/
└── README.md
```

## Setup

```bash
# Install Terraform
# Download from: https://www.terraform.io/downloads

# Initialize
cd terraform/production
terraform init

# Plan
terraform plan

# Apply
terraform apply
```
