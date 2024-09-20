from django.http import HttpResponseRedirect
from django.shortcuts import render

from dlo_client.dlo import (
    DLORequest,
    RedirectTargetCareprovider,
    RedirectTargetClient,
    UserType,
)
from dlo_client.forms import RedirectTargetCareproviderForm, RedirectTargetClientForm


def index(request):
    return render(
        request,
        "index.html",
        {
            "redirect_target_careprovider_form": RedirectTargetCareproviderForm,
            "redirect_target_client_form": RedirectTargetClientForm,
        },
    )


def redirect_to_professional_account(request):
    dlo_request = DLORequest(
        user_id="dirk+professional", usertype=UserType.CAREPROVIDER
    )
    target_url = dlo_request.generate_dlo_url()

    return HttpResponseRedirect(target_url)


def redirect_to_client_account(request):
    dlo_request = DLORequest(user_id="dirk+client", usertype=UserType.CLIENT)
    target_url = dlo_request.generate_dlo_url()

    return HttpResponseRedirect(target_url)


def redirect_to_professional_account_with_redirect_target(request):
    if request.method == "POST":
        redirect_form = RedirectTargetCareproviderForm(request.POST)
        if redirect_form.is_valid():
            selected_value = redirect_form.cleaned_data["redirect_target_field"]
            redirect = RedirectTargetCareprovider(selected_value)

            dlo_request = DLORequest(
                user_id="dirk+professional",
                usertype=UserType.CAREPROVIDER,
                redirect=redirect,
            )
            target_url = dlo_request.generate_dlo_url()

            return HttpResponseRedirect(target_url)


def redirect_to_client_account_with_redirect_target(request):
    if request.method == "POST":
        redirect_form = RedirectTargetClientForm(request.POST)
        if redirect_form.is_valid():
            selected_value = redirect_form.cleaned_data["redirect_target_field"]
            redirect = RedirectTargetClient(selected_value)

            dlo_request = DLORequest(
                user_id="dirk+client", usertype=UserType.CLIENT, redirect=redirect
            )
            target_url = dlo_request.generate_dlo_url()

            return HttpResponseRedirect(target_url)
