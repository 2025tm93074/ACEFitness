import os
import sqlite3

from flask import Flask, jsonify, request, render_template


DEFAULT_DB = "aceest_fitness.db"


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.path.join(app.root_path, DEFAULT_DB)
    )

    if test_config:
        app.config.update(test_config)

    def get_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db()

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                height REAL NOT NULL,
                weight REAL NOT NULL,
                program TEXT NOT NULL,
                calories INTEGER NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()

    with app.app_context():
        init_db()

    # ---------------------------------------------------------
    # FITNESS PROGRAMS
    # ---------------------------------------------------------

    programs = {
        "fat_loss": {
            "name": "Fat Loss",
            "calorie_factor": 22,
            "description": "Full-body training with a calorie-controlled diet."
        },
        "muscle_gain": {
            "name": "Muscle Gain",
            "calorie_factor": 35,
            "description": "Progressive resistance training focused on muscle growth."
        },
        "beginner": {
            "name": "Beginner",
            "calorie_factor": 26,
            "description": "Simple full-body training for beginners."
        }
    }

    # ---------------------------------------------------------
    # FRONTEND
    # ---------------------------------------------------------

    @app.route("/")
    def home():
        return render_template(
            "index.html",
            programs=programs
        )

    # ---------------------------------------------------------
    # HEALTH CHECK
    # ---------------------------------------------------------

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    # ---------------------------------------------------------
    # GET PROGRAMS
    # ---------------------------------------------------------

    @app.route("/programs", methods=["GET"])
    def get_programs():
        return jsonify(programs)

    # ---------------------------------------------------------
    # GET ALL CLIENTS
    # ---------------------------------------------------------

    @app.route("/clients", methods=["GET"])
    def get_clients():
        conn = get_db()

        rows = conn.execute(
            """
            SELECT id, name, age, height, weight, program, calories
            FROM clients
            ORDER BY id
            """
        ).fetchall()

        conn.close()

        clients = [dict(row) for row in rows]

        return jsonify(clients)

    # ---------------------------------------------------------
    # CREATE CLIENT
    # ---------------------------------------------------------

    @app.route("/clients", methods=["POST"])
    def create_client():

        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "error": "Request body must contain JSON."
                }
            ), 400

        required_fields = [
            "name",
            "age",
            "height",
            "weight",
            "program"
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in data
        ]

        if missing_fields:
            return jsonify(
                {
                    "error": "Missing required fields.",
                    "missing": missing_fields
                }
            ), 400

        program = data["program"]

        if program not in programs:
            return jsonify(
                {
                    "error": "Invalid program.",
                    "available_programs": list(programs.keys())
                }
            ), 400

        try:
            name = str(data["name"]).strip()
            age = int(data["age"])
            height = float(data["height"])
            weight = float(data["weight"])

        except (ValueError, TypeError):
            return jsonify(
                {
                    "error": "Invalid data type for client fields."
                }
            ), 400

        if not name:
            return jsonify(
                {
                    "error": "Name cannot be empty."
                }
            ), 400

        if age <= 0:
            return jsonify(
                {
                    "error": "Age must be greater than zero."
                }
            ), 400

        if height <= 0:
            return jsonify(
                {
                    "error": "Height must be greater than zero."
                }
            ), 400

        if weight <= 0:
            return jsonify(
                {
                    "error": "Weight must be greater than zero."
                }
            ), 400

        # Basic calorie calculation based on the
        # program factors from the original ACEest application.
        calorie_factor = programs[program]["calorie_factor"]
        calories = int(weight * calorie_factor)

        conn = get_db()

        cursor = conn.execute(
            """
            INSERT INTO clients
            (name, age, height, weight, program, calories)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                age,
                height,
                weight,
                program,
                calories
            )
        )

        conn.commit()

        client_id = cursor.lastrowid

        conn.close()

        return jsonify(
            {
                "id": client_id,
                "name": name,
                "age": age,
                "height": height,
                "weight": weight,
                "program": program,
                "calories": calories
            }
        ), 201

    # ---------------------------------------------------------
    # GET SINGLE CLIENT
    # ---------------------------------------------------------

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client(client_id):

        conn = get_db()

        row = conn.execute(
            """
            SELECT id, name, age, height, weight, program, calories
            FROM clients
            WHERE id = ?
            """,
            (client_id,)
        ).fetchone()

        conn.close()

        if row is None:
            return jsonify(
                {
                    "error": "Client not found."
                }
            ), 404

        return jsonify(dict(row))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )