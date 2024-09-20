import hashlib
import hmac
import os
import time
import uuid
from enum import StrEnum
from typing import Union, Optional
from urllib.parse import urlencode

from pydantic import BaseModel

BASE_URL = "https://ca-diroiaya.minddistrict.dev/"
REDIRECT_BASE_URL = "https://ca-diroiaya.minddistrict.dev/aux/frameredirect"


class UserType(StrEnum):
    CAREPROVIDER = "careprovider"
    CLIENT = "client"

class RedirectTargetCareprovider(StrEnum):
    TASKS = "tasks"
    MY_CLIENTS = "c"
    ALL_CLIENTS = "c/@@allclients"
    LIST_OF_PROFESSIONALS = "p"
    CONFIGURATION = "configuration"
    CATALOGUE = "catalogue"

class RedirectTargetClient(StrEnum):
    CATALOGUE = "catalogue"
    CONVERSATIONS = "conversations"

class DLORequest(BaseModel):
    user_id: str
    usertype: UserType
    redirect: Optional[Union[RedirectTargetCareprovider, RedirectTargetClient]] = None
    shared_secret_key: str = None

    def __init__(self, user_id, usertype, redirect=None):
        super().__init__(user_id=user_id, usertype=usertype, redirect=redirect)
        self.shared_secret_key = os.environ["SHARED_KEY_SECRET"]

    def generate_dlo_url(self) -> str:
        """
        Build the DLO URL
        Returns:
            The generated DLO URL
        """
        nonce = self._generate_nonce()
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        base_url = BASE_URL

        params = {
            "userid": self.user_id,
            "usertype": self.usertype,
            "nonce": nonce,
            "timestamp": timestamp,
        }

        if self.redirect:
            base_url = REDIRECT_BASE_URL
            params["redirect"] = f"{BASE_URL}{self.redirect.value}"

        # Generate the token
        token = self._generate_hmac_token(params, self.shared_secret_key)
        params["token"] = token

        # Generate the final URL
        dlo_url = f"{base_url}?{urlencode(params)}"
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
        message = "".join(f"{k}{v}" for k, v in sorted(params.items()))
        return hmac.new(
            secret_key.encode(), message.encode(), hashlib.sha512
        ).hexdigest()
