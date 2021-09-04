from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=False, label='Imię')
    last_name = forms.CharField(max_length=100, required=False, label='Nazwisko')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditForm(UserChangeForm):
    # powoduje brak formularza hasła z UserChangeForm
    password = None
    # pozwala edytować poniższe formy
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=False, label='Imię')
    last_name = forms.CharField(max_length=100, required=False, label='Nazwisko')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
