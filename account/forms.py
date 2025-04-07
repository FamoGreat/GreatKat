from django import forms
from .models import Account
from django.contrib.auth import authenticate


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirm Password',
        error_messages={'required': 'Please confirm your password'}
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'password': 'Password',
        }
        error_messages = {
            'first_name': {'required': 'First name is required'},
            'last_name': {'required': 'Last name is required'},
            'email': {
                'required': 'Email address is required',
                'invalid': 'Enter a valid email address',
            },
            'phone_number': {'required': 'Phone number is required'},
            'password': {'required': 'Password is required'},
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')


class LoginForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'email': 'Email Address',
            'password': 'Password',
        }

    # Custom validation to check if the email exists in the system
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required.')
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise forms.ValidationError('No account found with this email address.')
        return email

    # Custom validation for password
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Password is required.')
        return password

    # This method can be used to add further login validation, for example, checking if the password matches the one in the system
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Authenticate the user
        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data