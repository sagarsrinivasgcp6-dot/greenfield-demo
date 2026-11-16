# Task Manager Backend

A Task Manager backend API built with FastAPI, containerized with Docker, configured for Google Cloud Run deployment via Terraform, and automated with GitHub Actions and Cloud Build.

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Local Execution

Run the backend service locally with Uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

## Testing

Run unit tests:

```bash
python -m unittest discover -s tests -p test_*.py -v
```

Run integration tests:

```bash
python -m unittest discover -s tests -p test_*.py -v
```

## Deployment

Deploy infrastructure using Terraform:

```bash
terraform -chdir=infra/terraform init
```

## Smoke Testing

Verify that the service health endpoint responds:

```bash
curl -f http://localhost:8080/health
```

<!-- brownfield-executable-readme
{
  "version": 1,
  "environment": ["PORT"],
  "commands": [
    {
      "category": "setup",
      "command": "pip install -r requirements.txt",
      "verification": "static"
    },
    {
      "category": "local",
      "command": "uvicorn app:app --host 0.0.0.0 --port 8080",
      "verification": "static"
    },
    {
      "category": "backend",
      "command": "uvicorn app:app --host 0.0.0.0 --port 8080",
      "verification": "static"
    },
    {
      "category": "unit",
      "command": "python -m unittest discover -s tests -p test_*.py -v",
      "verification": "execute"
    },
    {
      "category": "integration",
      "command": "python -m unittest discover -s tests -p test_*.py -v",
      "verification": "execute"
    },
    {
      "category": "deploy",
      "command": "terraform -chdir=infra/terraform init",
      "verification": "static"
    },
    {
      "category": "smoke",
      "command": "curl -f http://localhost:8080/health",
      "verification": "static"
    }
  ],
  "not_applicable": {
    "frontend": "No frontend exists in this backend repository.",
    "e2e": "No E2E suite exists."
  }
}
-->
