# Task Manager Backend

A lightweight Task Manager backend built with FastAPI, Docker, and Google Cloud Run, provisioned using Terraform and automated with GitHub Actions and Cloud Build.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Local Execution

Run the backend application locally:

```bash
python app.py
```

## Testing

Run the unit tests:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

## GCP Deployment

Deploy infrastructure and service using Terraform:

```bash
terraform -chdir=infra/terraform apply -auto-approve
```

## Smoke Testing

Verify that the service is running and healthy:

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
      "category": "backend",
      "command": "python app.py",
      "verification": "static"
    },
    {
      "category": "unit",
      "command": "python -m unittest discover -s tests -p 'test_*.py' -v",
      "verification": "execute"
    },
    {
      "category": "deploy",
      "command": "terraform -chdir=infra/terraform apply -auto-approve",
      "verification": "static"
    },
    {
      "category": "smoke",
      "command": "curl -f http://localhost:8080/health",
      "verification": "static"
    }
  ],
  "not_applicable": {
    "local": "Local orchestration is identical to running the backend directly with python app.py.",
    "frontend": "No frontend exists in this backend repository.",
    "integration": "No integration test suite exists; unit tests cover endpoint contracts.",
    "e2e": "No end-to-end test suite exists."
  }
}
-->
