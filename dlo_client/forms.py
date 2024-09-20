from django import forms

from dlo_client.dlo import RedirectTargetCareprovider, RedirectTargetClient


class RedirectTargetCareproviderForm(forms.Form):
    """
    A choice field containing all redirect targets for professionals.
    """
    redirect_target_field = forms.ChoiceField(
        choices=[(tag.value, tag.value) for tag in RedirectTargetCareprovider]
    )


class RedirectTargetClientForm(forms.Form):
    """
    A choice field containing all redirect targets for clients.
    """
    redirect_target_field = forms.ChoiceField(
        choices=[(tag.value, tag.value) for tag in RedirectTargetClient]
    )
