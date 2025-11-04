# Fastapi url shortener

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
