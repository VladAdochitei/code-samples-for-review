# Terraform to deploy a fully functioning wordpress website with a RDS database

## 📦 **AWS WordPress Infrastructure with Terraform**
**Creator**: Vladut-Andrei Adochitei  
**Project Title**: `aws-terraform-wordpress`

---

### **Overview**

This project provisions a fully functional, production-ready WordPress hosting environment on AWS using **Terraform** and a **modular architecture**. It automates the setup of network infrastructure, compute, and database resources while offering configurable variables and reusable modules for flexibility and scalability.

---

### **Features & Components**

Using Terraform and AWS, this setup automatically provisions:

- **VPC and Networking**
  - 1 VPC
  - 1 Internet Gateway
  - 1 Public Subnet
  - 2 Private Subnets (required for RDS high availability)
  - 1 Public Route Table with association
  - 1 Subnet Group for RDS

- **Security**
  - 2 Security Groups: 
    - 1 for the DMZ/public access (e.g., EC2)
    - 1 for the private DB layer (RDS)

- **Compute & Storage**
  - 1 EC2 instance for the WordPress server
  - 1 Elastic IP for static public access

- **Database**
  - 1 Amazon RDS instance (MySQL/PostgreSQL)
  - Private subnet isolation for DB security

---

### **Architecture**

This infrastructure is broken into the following reusable modules:
- `vpc_submodule`: Manages all VPC-related resources
- `ec2_submodule`: Provisions and configures the EC2 instance
- `rds_submodule`: Deploys the RDS database in secure private subnets

Each module includes detailed documentation for input variables, enabling you to tailor the setup to your requirements.

---

### **Usage Instructions**

Before running, ensure you have the following installed:
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)  
  ```bash
  sudo apt install awscli
  aws configure
  ```
- [Terraform](https://developer.hashicorp.com/terraform/downloads)
  ```bash
  sudo apt install terraform
  ```

**Steps to deploy:**

```bash
git clone https://github.com/VladAdochitei/aws-terraform-wordpress
cd aws-terraform-wordpress

terraform init     # Initialize Terraform
terraform get      # Fetch module sources
terraform plan     # Review execution plan
terraform apply    # Deploy infrastructure
```

---

### **Deployment Logging**

To assist with debugging and verification:
- A status log file is created on the EC2 instance:
  ```bash
  /home/ec2-user/wordpress-deploy-status.txt
  ```
- The log is also exposed via HTTP:
  ```bash
  http://<EC2-PUBLIC-IP>/wordpress-deploy-status.html
  ```

---

### 📌 **Note**

Make sure to update the input variables (e.g., CIDR blocks, instance type, DB credentials) to suit your specific use case. All configuration is handled through well-documented variables across the module files.

---

### ✅ **Outputs**

After successful deployment, Terraform outputs:
- The public IP address of the WordPress server
- The associated Elastic IP

