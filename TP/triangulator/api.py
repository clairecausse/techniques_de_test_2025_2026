from flask import Flask, request, Response

def create_app():
    app = Flask(__name__)

    @app.get("/triangulate")
    def triangulate_endpoint():
        raise NotImplementedError("API not implemented yet")

    return app
