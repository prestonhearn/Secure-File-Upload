# Secure-File-Upload

## Overview
Secure File Upload is a FastAPI-based service to allow ease of file transfer from any device on the local network to the device running the Secure File Upload server.

## Project Goals
* Secure file upload handling
* Security scanning integration (future)
* Containerized deployment (future)

## Tech Stack
* Python
* FastAPI
* uv
* Git
* Docker
* Pytest
* GitHub Actions
* Trivy

## Getting Started
### Prerequisites
* uv installed
### Setup
`uv sync`
### Run Server Outside of Container
`uv run uvicorn main:app --host 0.0.0.0 --port 80 --reload`

## Security
![CI](https://github.com/YOURUSER/YOURREPO/actions/workflows/secure-ci.yml/badge.svg)
### CI Security Pipeline

Every commit is automatically verified with:

- Unit tests (pytest)
- Dependency vulnerability scanning (pip-audit)
- Container image scanning (Trivy)
- SBOM generation (CycloneDX)

Pull requests must pass all checks before merging.

## Project Status
Under development / Early stages