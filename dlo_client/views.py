from django.shortcuts import render

from django.http import HttpResponseRedirect

from dlo_client.dlo import DLORequest


def index(request):
    return render(request, 'index.html')
def my_view(request):
    dlo_request = DLORequest(user_id="dirk+professional", usertype="careprovider")
    target_url = dlo_request.generate_dlo_url()

    return HttpResponseRedirect(target_url)
