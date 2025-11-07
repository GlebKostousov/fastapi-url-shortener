# Fastapi url shortener

[![Python checks](https://img.shields.io/badge/Python-checks-passing?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/GlebKostousov/fastapi-url-shortener/actions/workflows/python-checks.yaml)
[![Python 3.13.1](https://img.shields.io/badge/Python-3.13.1-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3131/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Redis](https://img.shields.io/badge/Redis-6.0.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![uv](https://img.shields.io/badge/uv-0.9.7-DE5FE9?style=for-the-badge&logo=astral&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/Ruff-linter-FFC835?style=for-the-badge&logo=ruff&logoColor=black)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/MyPy-type%20checker-1f5490?style=for-the-badge&logo=python&logoColor=white)](http://mypy-lang.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-FAB040?style=for-the-badge&logo=pre-commit&logoColor=black)](https://pre-commit.com)
[![pytest](https://img.shields.io/badge/pytest-testing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)



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
