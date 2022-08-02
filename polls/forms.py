from django import forms


class RegisterForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', type='password', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.EmailField(label='First Name', max_length=100)
    last_name = forms.EmailField(label='Last Name', max_length=100)
