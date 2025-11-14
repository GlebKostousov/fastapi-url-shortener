"""Module for helps with working with Redis db with username and password"""

__all__ = ("redis_users",)

import logging
from typing import cast

from redis import Redis

from api.api_v1.auth.services.users_helper import AbstractUsersHelper
from core.config import settings

log = logging.getLogger(__name__)


class UserTokensHelper(AbstractUsersHelper):
    """Implementation of the AbstractUsersHelper interface for the
    login-password combination"""

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        *,
        decode_responses: bool = False,
    ) -> None:
        """
        init class

        Args:
            host (str): host url
            port (int): port to connect
            db (int): number of database in redis client
            decode_responses (bool): auto decode responses to UTF-8. If False - bytes
        """

        self.redis_users = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    def get_user_password(self, username: str) -> str | None:
        """
        Get password from db by username

        Args:
            username (str): username for getting password

        Returns:
            str | None: If username in db - return password else None

        """
        if not self.redis_users.exists(username):
            return None

        return cast("str | None", self.redis_users.get(name=username))

    def add_user(self, username: str, password: str) -> None:
        """
        Adds user and password to the database

        Args:
            username (str): login
            password (str): password

        Returns:

        """
        self.redis_users.set(name=username, value=password)


redis_users = UserTokensHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.users,
    decode_responses=True,
)
