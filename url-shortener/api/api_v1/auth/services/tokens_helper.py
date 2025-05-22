import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    """
    Что мне нужно от обертки
    - проверить на наличие токена
    - добавлять токен в хранилище
    - сгенерировать и добавить токены
    """

    @abstractmethod
    def get_all_tokens(self) -> list[str]:
        """
        Get all exist tokens in db
        :return: list of tokens
        """
        pass

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
