"""Module for helps with work with user tokens"""

import logging
from typing import cast

from redis import Redis

from core.config import settings
from services.auth.tokens_helper import AbstractTokensHelper

log = logging.getLogger(__name__)


class RedisTokensHelper(AbstractTokensHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        tokens_set_name: str,
        *,
        decode_responses: bool = False,
    ) -> None:

        self.tokens_set = tokens_set_name
        self.redis_tokens = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    def token_exists(self, token_to_check: str) -> bool:
        return bool(
            self.redis_tokens.sismember(
                self.tokens_set,
                token_to_check,
            ),
        )

    def delete_token(self, token_to_delete: str) -> None:
        self.redis_tokens.srem(
            self.tokens_set,
            token_to_delete,
        )

    def add_token(self, token_to_add: str) -> None:
        self.redis_tokens.sadd(self.tokens_set, token_to_add)

    def get_all_tokens(self) -> list[str]:
        return list(cast(set[str], self.redis_tokens.smembers(self.tokens_set)))


redis_tokens = RedisTokensHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.tokens,
    decode_responses=True,
    tokens_set_name=settings.redis.namespace.set_name.tokens,
)
