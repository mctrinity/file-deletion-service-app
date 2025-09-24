
from dotenv import load_dotenv
import os
# Load .env before any local imports
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, BadRequest
from .config import settings
from . import aws_delete, azure_delete


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    @app.post("/delete/aws")
    def delete_aws():
        data = _json()
        bucket = data.get("bucket")
        key = data.get("key")
        if not bucket or not key:
            raise BadRequest("body must include {bucket, key}")
        result = aws_delete.delete_object(bucket, key)
        return jsonify({"status": "success", **result})

    @app.post("/delete/azure")
    def delete_azure():
        data = _json()
        container = data.get("container")
        blob = data.get("blob")
        if not container or not blob:
            raise BadRequest("body must include {container, blob}")
        result = azure_delete.delete_blob(container, blob)
        return jsonify({"status": "success", **result})

    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            return jsonify({"status": "error", "message": e.description}), e.code
        # Normalize common errors
        msg = str(e)
        code = 404 if isinstance(e, FileNotFoundError) else 400
        return jsonify({"status": "error", "message": msg}), code

    return app


def _json():
    if not request.is_json:
        raise BadRequest("Content-Type must be application/json")
    return request.get_json()


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=settings.PORT, debug=settings.DEBUG)
