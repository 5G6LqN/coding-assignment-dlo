import os
from unittest import mock
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from pydantic_core import ValidationError

from dlo_client.dlo import DLORequest, UserType, RedirectTargetCareprovider, RedirectTargetClient


def test_generate_hmac_token():
    assert (
        DLORequest._generate_hmac_token({"a": "A"}, "12345")
        == "521125e97ad36e3c45f60946af98e29583512651aeaae2eb6947cfb36037978422256619d040a84d861ad375fa09e8e52f47297dfa6f57d2f9969e0081261fcc"
    )


@freeze_time("2024-09-20T14:05:43Z")
@mock.patch("dlo_client.dlo.DLORequest._generate_nonce")
@pytest.mark.parametrize(
    "usertype, expected_result",
    [
        (
            UserType.CAREPROVIDER,
            "https://ca-diroiaya.minddistrict.dev/?userid=XXX&usertype=careprovider&nonce=1726841143309&timestamp=2024-09-20T14%3A05%3A43Z&token=000a9db469fb0e82dc551326c2380652a3207a27cc29f36f5f1cd9e57fa2184356b4cf39b36d4d7fea84b11f2b02e57a88063a0469c1a90e8172b241315ed33c",
        ),
        (
            UserType.CLIENT,
            "https://ca-diroiaya.minddistrict.dev/?userid=XXX&usertype=client&nonce=1726841143309&timestamp=2024-09-20T14%3A05%3A43Z&token=08328094936695f2d3120f74bdc63379a72783af6554fdbf9da29905640ec8ffeeacf6bf332cdf829a587d86103e0bb8e9da82a9dcde88bc5d7a64d2fa97ceca",
        ),
    ],
)
def test_generate_dlo_url(mocked_generate_nonce, usertype, expected_result):
    """
    Compare the locally created URL to one created on
    https://docs.minddistrict.com/delegatedlogon/index.html

    Args:
        mocked_generate_nonce: mocked generate_nonce method so we can overwrite the return value
    """
    mocked_generate_nonce.return_value = "1726841143309"

    with patch.dict(os.environ, {"SHARED_KEY_SECRET": "12345"}):
        dlo_request = DLORequest(user_id="XXX", usertype=usertype)

    assert dlo_request.generate_dlo_url() == expected_result


def test_usertype_is_invalid():
    with pytest.raises(ValidationError):
        DLORequest(user_id="XXX", usertype="Wrong")


@freeze_time("2024-09-20T17:25:18Z")
@mock.patch("dlo_client.dlo.DLORequest._generate_nonce")
@pytest.mark.parametrize(
    "usertype, redirect_target, expected_result",
    [
        (
            UserType.CAREPROVIDER,
            RedirectTargetCareprovider.ALL_CLIENTS,
            "https://ca-diroiaya.minddistrict.dev/aux/frameredirect?userid=XXX&usertype=careprovider&nonce=1726841143309&timestamp=2024-09-20T17%3A25%3A18Z&redirect=https%3A%2F%2Fca-diroiaya.minddistrict.dev%2Fc%2F%40%40allclients&token=4bfa0de82255e2702916144dc701e003da39f95307835acb1b796de1a378975332a02a05ba1c5897911a97eff7be05e5347599598e5c00524c6c5f956211b5d9",
        ),
        (
            UserType.CLIENT,
            RedirectTargetClient.CATALOGUE,
            "https://ca-diroiaya.minddistrict.dev/aux/frameredirect?userid=XXX&usertype=client&nonce=1726841143309&timestamp=2024-09-20T17%3A25%3A18Z&redirect=https%3A%2F%2Fca-diroiaya.minddistrict.dev%2Fcatalogue&token=7c38baf264c87bb83c8d315aad8172683f454b4d685d381e6cbdf8e397fe4e45df5e801d18541307ae2957b586af77a818d4c998448a125c86e0748c0646eac8",
        ),
    ],
)
def test_generate_dlo_url_with_redirect(mocked_generate_nonce, usertype, redirect_target, expected_result):
    mocked_generate_nonce.return_value = "1726841143309"

    with patch.dict(os.environ, {"SHARED_KEY_SECRET": "12345"}):
        dlo_request = DLORequest(user_id="XXX", usertype=usertype, redirect=redirect_target)

    assert dlo_request.generate_dlo_url() == expected_result
