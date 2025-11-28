import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)
from starlette import status
from starlette.requests import Request

from services.auth import redis_tokens, redis_users

log = logging.getLogger(__name__)
UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
)
static_api_token = HTTPBearer(
    auto_error=False,
    scheme_name="Static Api Token",
    description="Your **Static Api Token** from developer portal. [Read more](#)",
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic user name + password auth",
    auto_error=False,
)


def validate_basic_auth(credentials: HTTPBasicCredentials | None) -> None:
    if credentials and redis_users.validate_user_password(
        username=credentials.username,
        password=credentials.password,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(
        credentials=credentials,
    )


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
) -> None:
    if redis_tokens.token_exists(api_token.credentials):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You API token is invalid.",
    )


def api_token_or_basic_auth_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    log.info("auth type: %s", "basic auth" if credentials else "api token")
    if request.method not in UNSAFE_METHODS:
        return None

    if credentials:
        log.info("credentials: %s", credentials)
        return validate_basic_auth(credentials=credentials)

    if api_token:
        log.info("api_token: %s", api_token)
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth required",
    )
