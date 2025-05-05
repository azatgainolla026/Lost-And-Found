import string

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User, Item, ClaimRequest


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        required=True,
        label='Password'
    )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['user', 'date_found', 'item_status']
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "cols": 40}),
            "tags": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "name": "Item Name",
            "description": "Full Description",
            "category": "Category",
            "location": "Location Found",
            "tags": "Tags",
            "image": "Upload Image",
        }


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            "placeholder": "Search Items",
            "class": "form-control",
            "style": "width: 100%;"
        })
    )

    def clean_search(self):
        search = self.cleaned_data.get("search", "").strip()
        search = search.translate(str.maketrans("", "", string.punctuation))
        if search and len(search) < 3:
            raise ValidationError("Search term must have at least 3 letters.")
        return search


class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a short message...'}),
        }
