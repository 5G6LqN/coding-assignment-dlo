import requests
from django.test import Client
from django.urls import reverse

from dlo_client.dlo import DLORequest, UserType


def test_redirect_to_professional_account():
    client = Client()
    redirect_response = client.post(reverse("redirect_to_professional_account"))

    response = requests.get(redirect_response.url)
    assert response.status_code == 200
    assert "You successfully logged in" in response.content.decode("utf-8")
    assert "Clients" in response.content.decode("utf-8")


def test_redirect_to_client_account():
    client = Client()
    redirect_response = client.post(reverse("redirect_to_client_account"))

    response = requests.get(redirect_response.url)
    assert response.status_code == 200
    assert "You successfully logged in" in response.content.decode("utf-8")
    assert "Download the app!" in response.content.decode("utf-8")


def test_login_fails():
    dlo_request = DLORequest(user_id="XXX", usertype=UserType.CLIENT)
    dlo_url = dlo_request.generate_dlo_url()

    response = requests.get(dlo_url)
    assert response.status_code == 200
    assert "Unable to log in" in response.content.decode("utf-8")


def test_redirect_to_professional_account_redirect_target():
    client = Client()
    url = reverse("redirect_to_professional_account_with_redirect_target")
    data = {"redirect_target_field": "tasks"}

    redirect_response = client.post(url, data)

    response = requests.get(redirect_response.url)
    assert response.status_code == 200
    assert "Tasks" in response.content.decode("utf-8")


def test_redirect_to_client_account_redirect_target():
    client = Client()
    url = reverse("redirect_to_client_account_with_redirect_target")
    data = {"redirect_target_field": "conversations"}

    redirect_response = client.post(url, data)

    response = requests.get(redirect_response.url)
    assert response.status_code == 200
    assert "Conversations" in response.content.decode("utf-8")
    assert "View all conversations" not in response.content.decode("utf-8")
