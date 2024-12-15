from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, BaseUserCreationForm
from accounts.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-2', })

        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2'})
        self.fields["username"].label = "Email"


class UserRegisterForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'birthday', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-2'})

        self.fields['birthday'].widget = forms.DateInput(attrs={'class': 'form-control mb-2', 'type': 'date'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2'})

    def clean_email(self):
        email = self.cleaned_data.get("email")

        return email
