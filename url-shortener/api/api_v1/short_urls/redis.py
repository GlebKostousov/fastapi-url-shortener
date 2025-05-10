import secrets

from redis import Redis
from abc import ABC, abstractmethod

from core import config
import logging

log = logging.getLogger(__name__)


class AbstractTokensHelper(ABC):
    """
    Что мне нужно от обертки
    - проверить на наличие токена
    - добавлять токен в хранилище
    - сгенерировать и добавить токены
    """

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """
        Check if token exists
        """

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Save token in storage
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        """
        Generate token
        """
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        """
        Generate and save token
        """
        token = self.generate_token()
        self.add_token(token)
        return token


class RedisTokensHelper(AbstractTokensHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        tokens_set_name: str,
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
            )
        )

    def add_token(self, token_to_add: str) -> None:
        self.redis_tokens.sadd(self.tokens_set, token_to_add)


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    decode_responses=True,
    tokens_set_name=config.REDIS_TOKENS_SET_NAME,
)
