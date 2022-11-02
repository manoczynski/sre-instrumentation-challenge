from typing import Dict
from flask import Blueprint, jsonify, request, Response
from flask.typing import ResponseReturnValue
from prometheus_client import Summary

import random
import time

from .metrics import (
    request_total,
    response_status_code_total,
    response_status_code,
)
    

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('http_request_duration_seconds', 'Time spent processing request')

bucket_blueprint = Blueprint("zones", __name__)

data: Dict[str, bytes] = {}

@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)


@bucket_blueprint.route("/buckets/<id>")
def get_bucket(id: str) -> ResponseReturnValue:
    if id in data.keys():
        process_request(random.random())
        response_status_code_total.labels('/buckets', 'get', '200').inc()
        return data.get(id), 200, {"Content-Type": "application/octet-stream"}

    process_request(random.random())
    response_status_code_total.labels('/buckets', 'get', '404').inc()
    return jsonify({"error": "not found"}), 404, {"Content-Type": "application/json"}


@bucket_blueprint.route("/buckets/<id>", methods=["PUT"])
def put_bucket(id: str) -> ResponseReturnValue:
    data[id] = request.get_data()
    response_status_code_total.labels('/buckets', 'put', '200').inc()
    process_request(random.random())
    return "", 200



@bucket_blueprint.route("/buckets/<id>", methods=["DELETE"])
def delete_bucket(id: str) -> ResponseReturnValue:
    if id in data.keys():
        data.pop(id, None)
        process_request(random.random())
        response_status_code_total.labels('/buckets', 'delete', '500').inc()
        return "", 500

    process_request(random.random())
    response_status_code_total.labels('/buckets', 'delete', '400').inc()
    return jsonify({"error": "bad request"}), 400, {"Content-Type": "application/json"}
