from django import forms

from dlo_client.dlo import UserType


class UserTypeSelectorForm(forms.Form):
    user_type_selector_field = forms.ChoiceField(
        #choices=[(tag.name, tag.value) for tag in UserType]
        choices=[(UserType.CAREPROVIDER, "Care Provider"), (UserType.CLIENT, "Client")]
    )