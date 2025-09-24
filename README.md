# File Deletion Service (App)

Small Flask API to delete files from **AWS S3** and **Azure Blob Storage**.

## Endpoints

- `GET /healthz` → health check
- `POST /delete/aws` → `{ "bucket": "...", "key": "..." }`
- `POST /delete/azure` → `{ "container": "...", "blob": "..." }`

## Local Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DEBUG=true PORT=8080
# AWS creds via env or profile; Azure via connection string or account URL + MSI
python -m app.app
```
