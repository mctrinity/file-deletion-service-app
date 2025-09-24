# Cloud Storage Setup Guide: Azure Blob & AWS S3

This guide covers the initial setup for Azure and AWS authentication, and the creation of storage resources for use with your file deletion service.

---


## Azure Authentication

### Option 1: Connection String (Recommended for Dev/Test)
No extra authentication steps are needed. The connection string contains all required credentials.

### Option 2: Azure AD (Account URL, for Production)
1. Assign your user or service principal the **Storage Blob Data Contributor** role on the storage account:
  - Go to the Azure Portal → Storage Account → Access control (IAM)
  - Add role assignment → Storage Blob Data Contributor → select your user/service principal
2. If running locally, login with Azure CLI:
  ```sh
  az login
  ```
3. If running in Kubernetes in Azure, use a managed identity and assign it the same role.

---

### 1. Create a Storage Account
- Go to the [Azure Portal](https://portal.azure.com/)
- Search for **Storage accounts** and click **Create**
- Fill in the required fields (resource group, name, region, etc.)
- Click **Review + create** and then **Create**

### 2. Create a Container
- In your storage account, go to **Containers**
- Click **+ Container**
- Name it (e.g., `testfiles`) and set access level (private recommended)

### 3. Get the Connection String
- In your storage account, go to **Access keys**
- Copy the **Connection string** for use in your Kubernetes secret or `.env` file

### 4. Upload a Test Blob
- Install Azure CLI: https://docs.microsoft.com/cli/azure/install-azure-cli
- Login: `az login`
- Upload a file:
  ```sh
  echo "hello" > test.txt
  az storage blob upload \
    --account-name <your-account-name> \
    --container-name testfiles \
    --name test.txt \
    --file test.txt \
    --auth-mode key
  ```

---


## AWS Authentication

### Option 1: Access Key/Secret (Recommended for Dev/Test)
1. Create an IAM user with **Programmatic access**
2. Attach the **AmazonS3FullAccess** policy (or restrict as needed)
3. Use the access key and secret in your `.env` or Kubernetes secret

### Option 2: IAM Role (for Production in AWS)
1. Create an IAM role with S3 permissions
2. Attach the role to your EC2 instance, ECS task, or EKS service account
3. No need to set access keys in environment variables

---

### 1. Create an S3 Bucket
- Go to the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/home)
- Click **Create bucket**
- Enter a unique name (e.g., `your-unique-bucket-2025`)
- Choose region and settings, then create

### 2. Create or Use IAM Credentials
- Go to [IAM Console](https://console.aws.amazon.com/iam/)
- Create a user with **Programmatic access**
- Attach the **AmazonS3FullAccess** policy (or restrict as needed)
- Save the **Access Key ID** and **Secret Access Key**

### 3. Configure AWS CLI (optional, for local testing)
```sh
aws configure
# Enter your access key, secret key, region, and output format
```

### 4. Upload a Test File
```sh
echo "hello" > test.txt
aws s3 cp test.txt s3://your-unique-bucket-2025/test.txt
```

---

## Environment Variables for Your App

### Azure (use one method only)
- **Connection String (recommended for dev):**
  ```env
  AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=... # from Azure Portal
  ```
- **Account URL (for Azure AD/Managed Identity):**
  ```env
  AZURE_STORAGE_ACCOUNT_URL=https://<your-account>.blob.core.windows.net/
  # Requires Azure AD authentication and correct RBAC
  ```

### AWS
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

---

_This guide is intended for developers setting up cloud storage for use with a file deletion microservice in local or Kubernetes environments._
