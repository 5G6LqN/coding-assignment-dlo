import hashlib
import hmac
import os
import time
import uuid
from enum import StrEnum
from urllib.parse import urlencode

from pydantic import BaseModel

BASE_URL = "https://ca-diroiaya.minddistrict.dev/"


class UserType(StrEnum):
    PROFESSIONAL = "careprovider"
    CLIENT = "client"


class DLORequest(BaseModel):
    user_id: str
    usertype: UserType
    redirect: str = None
    shared_secret_key: str = None

    def __init__(self, user_id, usertype):
        super().__init__(user_id=user_id, usertype=usertype)
        self.shared_secret_key = os.environ['SHARED_KEY_SECRET']

    def generate_dlo_url(self) -> str:
        """
        Build the DLO URL
        Returns:
            The generated DLO URL
        """
        nonce = self._generate_nonce()
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

        params = {
            'userid': self.user_id,
            'usertype': self.usertype,
            'nonce': nonce,
            'timestamp': timestamp
        }

        if self.redirect:
            params['redirect'] = self.redirect

        # Generate the token
        token = self._generate_hmac_token(params, self.shared_secret_key)
        params['token'] = token

        # Generate the final URL
        dlo_url = f"{BASE_URL}?{urlencode(params)}"
        return dlo_url

    @staticmethod
    def _generate_nonce() -> str:
        """
        Generate a random nonce.

        Returns:
            str: The generated nonce
        """
        return uuid.uuid4()

    @staticmethod
    def _generate_hmac_token(params: dict, secret_key: str):
        """
        Generate an HMAC token for DLO using the secret key provided.

        Args:
            params: Dictionary of parameters to be hashed
            secret_key: The shared secret key

        Returns:
            str: The HMAC token
        """
        message = ''.join(f'{k}{v}' for k, v in sorted(params.items()))
        return hmac.new(secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
