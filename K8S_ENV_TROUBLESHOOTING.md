# Kubernetes Azure/AWS Environment Variable Troubleshooting Guide

This guide documents the troubleshooting steps for getting Azure and AWS environment variables working in a Kubernetes deployment for a file deletion service.

## Common Issues
- The application does not pick up the correct Azure or AWS credentials.
- Both `AZURE_STORAGE_CONNECTION_STRING` and `AZURE_STORAGE_ACCOUNT_URL` are present, causing Azure AD authentication to be used instead of the connection string.
- Environment variables are not updated in the running pod after secret/configmap changes.

## Step-by-Step Troubleshooting

### 1. Check Your Kubernetes Secrets and ConfigMaps
- Ensure your `k8s/secret.local.yaml` contains **only** the variables you want to use.
- For Azure, use only one of the following (prefer connection string for local/dev):
  ```yaml
  stringData:
    AZURE_STORAGE_CONNECTION_STRING: "<your-connection-string>"
    # Do NOT include AZURE_STORAGE_ACCOUNT_URL
  ```
- For AWS, include your keys if not using IAM roles:
  ```yaml
  stringData:
    AWS_ACCESS_KEY_ID: "<your-access-key>"
    AWS_SECRET_ACCESS_KEY: "<your-secret-key>"
  ```

### 2. Apply and Restart
- Apply your updated secret and configmap:
  ```sh
  kubectl apply -f k8s/secret.local.yaml
  kubectl apply -f k8s/configmap.yaml
  kubectl -n file-deletion rollout restart deploy file-deletion-svc
  ```

### 3. Verify Pod Environment Variables
- Check which Azure variables are present in your running pod:
  ```sh
  kubectl -n file-deletion exec deploy/file-deletion-svc -- printenv | grep AZURE_STORAGE
  ```
- You should see **only** `AZURE_STORAGE_CONNECTION_STRING` for connection string auth.
- If you see both, check all secrets/configmaps for stray `AZURE_STORAGE_ACCOUNT_URL` entries.

### 4. Test Your Endpoints
- Port-forward your service:
  ```sh
  kubectl -n file-deletion port-forward deploy/file-deletion-svc 8080:8080
  ```
- Test Azure deletion:
  ```sh
  curl -X POST http://localhost:8080/delete/azure \
    -H "Content-Type: application/json" \
    -d '{"container":"testfiles","blob":"test.txt"}'
  ```
- Test AWS deletion:
  ```sh
  curl -X POST http://localhost:8080/delete/aws \
    -H "Content-Type: application/json" \
    -d '{"bucket":"your-bucket","key":"test.txt"}'
  ```

### 5. If Problems Persist
- Double-check all secrets and configmaps:
  ```sh
  kubectl -n file-deletion get secret app-secrets -o yaml
  kubectl -n file-deletion get configmap app-config -o yaml
  ```
- Delete and re-create secrets if needed:
  ```sh
  kubectl -n file-deletion delete secret app-secrets
  kubectl apply -f k8s/secret.local.yaml
  kubectl -n file-deletion rollout restart deploy file-deletion-svc
  ```
- Make sure your Dockerfile does **not** set any Azure/AWS environment variables by default.

## Summary
- Only one Azure authentication method should be present in the pod environment.
- Always restart your deployment after updating secrets/configmaps.
- Use `printenv` in the pod to verify the environment.

---

_This guide was generated from a real troubleshooting session for a file deletion service using AWS S3 and Azure Blob Storage in Kubernetes._
