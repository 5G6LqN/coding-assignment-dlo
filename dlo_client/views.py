from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from dlo_client.dlo import DLORequest, UserType


def index(request):
    return render(request, "index.html")


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


def redirect_to_minddistrict_app_bak(request):
    if request.method == "POST":
        user_type_selector_form = UserTypeSelectorForm(request.POST)
        if form.is_valid():
            usertype = user_type_selector_form.cleaned_data["user_type_selector_field"]
            dlo_request = DLORequest(user_id="dirk+professional", usertype=usertype)
            target_url = dlo_request.generate_dlo_url()

            return HttpResponseRedirect(target_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserTypeSelectorForm()

    return render(request, "index.html", {"form": form})
