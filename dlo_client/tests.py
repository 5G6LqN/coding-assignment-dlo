from freezegun import freeze_time

from dlo_client.dlo import DLORequest


def test_generate_hmac_token():
    assert DLORequest._generate_hmac_token({}, "12345")

@freeze_time("2024-09-19T17:36:12Z")
def test_generate_dlo_url():
    dlo_request = DLORequest(user_id="XXX", usertype="careprovider")

    expected_result = "https://ca-diroiaya.minddistrict.dev/?userid=XXX&usertype=careprovider&nonce=1726767372005&timestamp=2024-09-19T17%3A36%3A12Z&token=27771012055985f9c88bfd05403dc9ccf0db4aba40799bff70e311cd62cd66403366922d403d11874db1b08a923df88162908dd060a3e1852d747bb5689a3699"

    assert dlo_request.generate_dlo_url() == expected_result

def test_generate_dlo_url_professional():
    dlo_request = DLORequest(user_id="dirk+professional", usertype="careprovider")

    expected_result = "https://ca-diroiaya.minddistrict.dev/?userid=XXX&usertype=careprovider&nonce=1726767372005&timestamp=2024-09-19T17%3A36%3A12Z&token=27771012055985f9c88bfd05403dc9ccf0db4aba40799bff70e311cd62cd66403366922d403d11874db1b08a923df88162908dd060a3e1852d747bb5689a3699"

    assert dlo_request.generate_dlo_url() == expected_result

def test_generate_dlo_url_client():
    dlo_request = DLORequest(user_id="dirk+client", usertype="client")

    expected_result = "https://ca-diroiaya.minddistrict.dev/?userid=XXX&usertype=careprovider&nonce=1726767372005&timestamp=2024-09-19T17%3A36%3A12Z&token=27771012055985f9c88bfd05403dc9ccf0db4aba40799bff70e311cd62cd66403366922d403d11874db1b08a923df88162908dd060a3e1852d747bb5689a3699"

    assert dlo_request.generate_dlo_url() == expected_result