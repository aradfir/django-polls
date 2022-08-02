import django.contrib.auth.models
from django import forms
from django.forms import ModelForm


class RegisterForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class RegisterForm2(ModelForm):
    class Meta:
        model = django.contrib.auth.models.User
        fields= ['username','password','email','first_name','last_name']
