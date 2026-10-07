# ACEest Fitness & Gym

A Flask-based fitness management application developed as part of the DevOps assignment.

The application provides a simple web interface for managing fitness clients and assigning them basic fitness programs. It uses SQLite for data persistence and includes automated testing, Docker containerization, Jenkins CI, and GitHub Actions CI.

---

## Features

- Flask web application
- Basic web-based frontend
- Add fitness clients
- View all registered clients
- Store client information using SQLite
- Fitness programs:
  - Fat Loss
  - Muscle Gain
  - Beginner
- Basic calorie calculation based on the selected program
- REST API endpoints
- Automated testing using Pytest
- Docker containerization
- Jenkins CI pipeline
- GitHub Actions CI pipeline

---

## Project Structure

```text
ACEest-Fitness-DevOps/
│
├── .github/
│   └── workflows/
│       └── main.yml
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── tests/
│   └── test_app.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── app.py
└── requirements.txt

```
### Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Pytest
- Git
- GitHub
- Docker
- Jenkins
- GitHub Actions
### Local Setup
1. Clone the repository
git clone https://github.com/2025tm93074/ACEest-Fitness-DevOps.git
cd ACEest-Fitness-DevOps

2. Install dependencies
The project dependencies are listed in requirements.txt.
python -m pip install -r requirements.txt

The main dependencies are:
Flask
pytest

3. Run the application
python app.py

The Flask application runs on port 5000.
Open the following URL in a browser:
http://localhost:5000

### Using the Application
The application provides a basic dashboard where a user can add fitness clients.
Client information includes:
- Name
- Age
- Height
- Weight
- Fitness program
After adding a client, the client appears in the client list.
The application stores client information in an SQLite database.
Available API Endpoints
Although the application provides a web interface, the underlying Flask application also exposes REST endpoints.
### Home
## GET /

Returns the application homepage.
### Health Check
## GET /health

Returns the application health status.
### Get Programs
## GET /programs

Returns the available fitness programs.
### Get Clients
## GET /clients

Returns all clients.
### Create Client
## POST /clients

Creates a new client.
Example request:
{
    "name": "John Doe",
    "age": 25,
    "height": 175,
    "weight": 70,
    "program": "fat_loss"
}

### Get Individual Client
## GET /clients/<client_id>

Returns information for a specific client.

### Running Tests
The project uses Pytest for automated testing.
Run:
python -m pytest -v

The tests cover:
- Home page
- Health check
- Fitness programs
- Client creation
- Client retrieval
- Non-existent clients
- Missing fields
- Invalid programs
- Invalid data types
- Invalid client values
The tests use a temporary SQLite database so that the application's normal database is not modified during testing.
Docker
Build the Docker image
From the project directory:
docker build -t aceest-fitness .

Run the application
docker run -p 5000:5000 aceest-fitness

Open:
http://localhost:5000

The application can then be accessed through the browser while running inside the Docker container.
Jenkins CI
Jenkins is used as a build and quality gate.
The Jenkins pipeline performs the following steps:
``` GitHub
   ↓
Checkout feature branch
   ↓
Install Python dependencies
   ↓
Run Pytest
   ↓
Build Docker image
``` 
The Jenkins job is configured to automatically check the GitHub repository for changes to the feature branch.
A successful Jenkins build confirms that:
- The latest source code can be checked out.
- Dependencies can be installed.
- Automated tests pass.
- The Docker image can be built successfully.
The Docker image produced by Jenkins is stored locally on the Jenkins VM.
GitHub Actions CI
GitHub Actions provides an automated CI workflow through:
.github/workflows/main.yml

The workflow is triggered on:
- Push
- Pull request
The workflow contains three stages:
```Build & Lint
      ↓
Docker Image Assembly
      ↓
Automated Testing

Build & Lint
```
The workflow:
- Checks out the repository.
- Sets up Python.
- Installs dependencies.
- Compiles the Python application.
- Checks Python syntax.
Docker Image Assembly
The workflow builds the Docker image using the project's Dockerfile.
Automated Testing
The Docker image is started and Pytest is executed inside the container.
This verifies that the automated tests work in the same containerized environment used by the application.
Git Workflow
Development is performed locally and changes are pushed to GitHub.
The current development workflow is:
```
Local Development
       ↓
Git Commit
       ↓
Git Push
       ↓
GitHub Feature Branch
       ↓
Jenkins CI
       ↓
GitHub Actions CI

```
The project uses meaningful commits to track application development, testing, Docker configuration, and CI configuration.
Docker and Jenkins Environment
The application can be run on the provided VM using Docker.
The Jenkins server on the VM pulls the project from GitHub, runs the tests, and builds the Docker image.
The Docker container can then be started on the VM using:


docker run -d \
  --name aceest-fitness \
  -p 5000:5000 \
  aceest-fitness:jenkins

The application can then be accessed through:
http://localhost:5000

when accessed from the VM itself.
### Notes
The SQLite database file is intentionally excluded from Git using .gitignore.
The Python virtual environment is also excluded from Git.
Docker builds the application from the source code and creates its own application environment.