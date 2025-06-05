import logging
from typing import cast

from redis import Redis

from api.api_v1.auth.services.users_helper import AbstractUsersHelper
from core import config

log = logging.getLogger(__name__)


class UserTokensHelper(AbstractUsersHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        decode_responses: bool = False,
    ) -> None:

        self.redis_users = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    def get_user_password(self, username: str) -> str | None:
        if not self.redis_users.exists(username):
            return None

        return cast(str | None, self.redis_users.get(name=username))

    def add_user(self, username: str, password: str) -> None:
        self.redis_users.set(name=username, value=password)

    # validate_user_password используй для проверки пароля


redis_users = UserTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USERS,
    decode_responses=True,
)
