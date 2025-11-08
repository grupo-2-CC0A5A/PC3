from flask import Flask, jsonify, request
from datetime import datetime
from decimal import Decimal
import json
import os


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.secret_key = os.environ.get("SECRET_KEY", "foobar")

    app.rentals = {}
    app.damage_catalog = {
        "Broca rota": Decimal("80.00"),
        "Carcasa rayada": Decimal("30.00"),
    }

    from routes import rental_bp

    app.register_blueprint(rental_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
