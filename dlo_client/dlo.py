import hmac
import hashlib
import os
import uuid
from datetime import datetime

from pydantic import BaseModel
from urllib.parse import urlencode
import time

BASE_URL = "https://ca-diroiaya.minddistrict.dev/"


class DLORequest(BaseModel):
    user_id: str
    usertype: str
    redirect: str = None
    shared_secret_key: str = os.environ['SHARED_KEY_SECRET']

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

    @staticmethod
    def _generate_nonce() -> str:
        """
        Generate a random nonce.

        Returns:
            str: The generated nonce
        """
        return uuid.uuid4()


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