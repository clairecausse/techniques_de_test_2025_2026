import requests
from flask import Flask, Response, jsonify, request

from triangulator.binary import (
    decode_point_set,
    encode_triangles,
)
from triangulator.triangulation import triangulate

POINTSET_MANAGER_URL = "http://localhost:5001/pointset"

def create_app():
    app = Flask(__name__)

    @app.get("/triangulate")
    def triangulate_endpoint():
        set_id = request.args.get("set_id")

        if set_id is None:
            return jsonify({"error": "Missing set_id"}), 400

        if not set_id.isdigit():
            return jsonify({"error": "Invalid set_id"}), 400

        resp = requests.get(f"{POINTSET_MANAGER_URL}/{set_id}")

        if resp.status_code != 200:
            return jsonify({"error": "PointSetManager failure"}), 502

        points = decode_point_set(resp.content)
        triangles = triangulate(points)

        binary = encode_triangles(points, triangles)
        return Response(binary, content_type="application/octet-stream")

    return app
