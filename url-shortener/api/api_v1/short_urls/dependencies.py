import logging
from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from api.api_v1.auth.services import (
    redis_tokens,
    redis_users,
)
from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
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


def prefetch_short_urls(slug: str) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
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
        return

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
