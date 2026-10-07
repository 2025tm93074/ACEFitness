import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    """
    Create a fresh Flask application for testing.

    A temporary SQLite database is used so that
    tests do not modify the real application database.
    """

    db_path = tmp_path / "test.db"

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(db_path),
        }
    )

    yield app


@pytest.fixture
def client(app):
    """
    Flask test client used to make requests
    without running the actual web server.
    """

    return app.test_client()


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"ACEest Fitness & Gym" in response.data


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy"
    }


# ---------------------------------------------------------
# PROGRAMS
# ---------------------------------------------------------

def test_get_programs(client):
    response = client.get("/programs")

    assert response.status_code == 200

    data = response.get_json()

    assert "fat_loss" in data
    assert "muscle_gain" in data
    assert "beginner" in data


# ---------------------------------------------------------
# CREATE CLIENT
# ---------------------------------------------------------

def test_create_client(client):

    response = client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": 25,
            "height": 175,
            "weight": 70,
            "program": "fat_loss"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "John Doe"
    assert data["age"] == 25
    assert data["height"] == 175
    assert data["weight"] == 70
    assert data["program"] == "fat_loss"

    # 70 kg * 22 calorie factor
    assert data["calories"] == 1540

    assert "id" in data


# ---------------------------------------------------------
# GET CLIENTS
# ---------------------------------------------------------

def test_get_clients(client):

    client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": 25,
            "height": 175,
            "weight": 70,
            "program": "fat_loss"
        }
    )

    response = client.get("/clients")

    assert response.status_code == 200

    clients = response.get_json()

    assert len(clients) == 1
    assert clients[0]["name"] == "John Doe"


# ---------------------------------------------------------
# GET SINGLE CLIENT
# ---------------------------------------------------------

def test_get_single_client(client):

    create_response = client.post(
        "/clients",
        json={
            "name": "Jane Doe",
            "age": 30,
            "height": 165,
            "weight": 60,
            "program": "beginner"
        }
    )

    client_id = create_response.get_json()["id"]

    response = client.get(
        f"/clients/{client_id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == client_id
    assert data["name"] == "Jane Doe"


# ---------------------------------------------------------
# CLIENT NOT FOUND
# ---------------------------------------------------------

def test_get_nonexistent_client(client):

    response = client.get("/clients/9999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Client not found."


# ---------------------------------------------------------
# MISSING REQUIRED FIELD
# ---------------------------------------------------------

def test_create_client_missing_field(client):

    response = client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": 25,
            "height": 175,
            "weight": 70
            # program intentionally missing
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "program" in data["missing"]


# ---------------------------------------------------------
# INVALID PROGRAM
# ---------------------------------------------------------

def test_create_client_invalid_program(client):

    response = client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": 25,
            "height": 175,
            "weight": 70,
            "program": "invalid_program"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid program."


# ---------------------------------------------------------
# INVALID DATA TYPE
# ---------------------------------------------------------

def test_create_client_invalid_data_type(client):

    response = client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": "twenty-five",
            "height": 175,
            "weight": 70,
            "program": "fat_loss"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid data type for client fields."


# ---------------------------------------------------------
# EMPTY NAME
# ---------------------------------------------------------

def test_create_client_empty_name(client):

    response = client.post(
        "/clients",
        json={
            "name": "",
            "age": 25,
            "height": 175,
            "weight": 70,
            "program": "fat_loss"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Name cannot be empty."


# ---------------------------------------------------------
# INVALID AGE
# ---------------------------------------------------------

def test_create_client_invalid_age(client):

    response = client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": 0,
            "height": 175,
            "weight": 70,
            "program": "fat_loss"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Age must be greater than zero."


# ---------------------------------------------------------
# INVALID WEIGHT
# ---------------------------------------------------------

def test_create_client_invalid_weight(client):

    response = client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": 25,
            "height": 175,
            "weight": 0,
            "program": "fat_loss"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Weight must be greater than zero."