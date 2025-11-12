# FastAPI URL Shortener

### Lib version

[![Python 3.13.1](https://img.shields.io/badge/Python-3.13.1-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3131/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-3776AB?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

[![Redis](https://img.shields.io/badge/Redis-6.0.0-3776AB?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![uv](https://img.shields.io/badge/uv-0.9.7-3776AB?style=for-the-badge&logo=astral&logoColor=white)](https://docs.astral.sh/uv/)

### Codestyle

[![Ruff](https://img.shields.io/badge/Ruff-strict-FAB040?style=for-the-badge&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/MyPy-strict-FAB040?style=for-the-badge&logo=python&logoColor=white)](http://mypy-lang.org)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-FAB040?style=for-the-badge&logo=pre-commit&logoColor=white)](https://pre-commit.com)

### Testing

[![pytest](https://img.shields.io/badge/pytest-testing-FAB040?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)
[![Coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FGlebKostousov%2F8ccc9117a4a81627856cb5d379113e0f%2Fraw%2Fcoverage.json&style=for-the-badge&logo=codecov&logoColor=white)](https://github.com/GlebKostousov/fastapi-url-shortener/actions/workflows/python-checks.yaml)

### GitHub Action

[![Python checks](https://img.shields.io/badge/Testing_and_code_style-On_PR-FAB040?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/GlebKostousov/fastapi-url-shortener/actions/workflows/python-checks.yaml)


## Develop

### Setup:

Right click   `url-shortener` -> Mark directory as -> Sources root

### Configure pre-commit

### Install

Install packages:

```shell
uv install
```

Install pre-commit hook:

```shell
pre-commit install
```

### Run

Go to workdir

```shell
cd url-shortener
```

Run DEV server

```shell
fastapi dev
```

## snippets

```shell
python -c 'import secrets; print(secrets.token_urlsafe(16))'
```
