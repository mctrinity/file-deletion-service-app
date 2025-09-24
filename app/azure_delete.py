from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from .config import settings


def _blob_service():
    """
    Prefers connection string; falls back to DefaultAzureCredential (MSI/Workload ID).
    Provide AZURE_STORAGE_CONNECTION_STRING OR AZURE_STORAGE_ACCOUNT_URL.
    """
    if settings.AZURE_STORAGE_CONNECTION_STRING:
        return BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )
    if settings.AZURE_STORAGE_ACCOUNT_URL:
        cred = DefaultAzureCredential(exclude_interactive_browser_credential=True)
        return BlobServiceClient(
            account_url=settings.AZURE_STORAGE_ACCOUNT_URL, credential=cred
        )
    raise ValueError("Set AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_URL")


def delete_blob(container: str, blob: str):
    if not container or not blob:
        raise ValueError("container and blob are required")
    svc = _blob_service()
    client = svc.get_container_client(container)
    try:
        client.get_blob_client(blob).delete_blob()
    except ResourceNotFoundError:
        raise FileNotFoundError(f"Blob not found: {container}/{blob}")
    return {"container": container, "blob": blob}
