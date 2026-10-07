"""Flask application for the username availability checker."""

from flask import Flask, jsonify, render_template, request

from src.username_manager import UsernameManager


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(MAX_USERNAME_LENGTH=24, LOAD_SAMPLE_DATA=True)
    if test_config:
        app.config.update(test_config)

    manager = UsernameManager(max_length=app.config["MAX_USERNAME_LENGTH"])
    if app.config["LOAD_SAMPLE_DATA"]:
        manager.load_sample_data()
    app.extensions["username_manager"] = manager

    def manager_for_request():
        return app.extensions["username_manager"]

    def request_username():
        payload = request.get_json(silent=True) or {}
        return payload.get("username")

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/stats")
    def stats():
        return jsonify(manager_for_request().statistics())

    @app.post("/api/check")
    def check_username():
        try:
            return jsonify(manager_for_request().check(request_username()))
        except ValueError as error:
            return jsonify(success=False, error=str(error)), 400

    @app.post("/api/add")
    def add_username():
        try:
            return jsonify(manager_for_request().add(request_username()))
        except ValueError as error:
            return jsonify(success=False, error=str(error)), 400

    @app.delete("/api/delete")
    def delete_username():
        try:
            return jsonify(manager_for_request().delete(request_username()))
        except ValueError as error:
            return jsonify(success=False, error=str(error)), 400

    @app.post("/api/sample")
    def load_sample():
        total = manager_for_request().load_sample_data()
        return jsonify(success=True, loaded=total, stats=manager_for_request().statistics())

    @app.post("/api/reset")
    def reset():
        manager_for_request().reset()
        return jsonify(success=True, stats=manager_for_request().statistics())

    @app.get("/api/buckets")
    def buckets():
        table = manager_for_request().hash_table
        return jsonify(buckets=table.occupied_buckets())

    @app.get("/api/bucket/<int:index>")
    def bucket(index):
        try:
            usernames = manager_for_request().hash_table.bucket_contents(index)
        except IndexError:
            return jsonify(success=False, error="Bucket index is outside the table."), 404
        return jsonify(index=index, usernames=usernames)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)