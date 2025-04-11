from django import forms
from order.models import Order 
from django.core.validators import EmailValidator


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'order_note': forms.Textarea(attrs={'class': 'form-control'}),
        }

    error_messages = {
            'first_name': {
                'required': 'First name is required',
            },
            'last_name': {
                'required': 'Last name is required',
            },
            'phone': {
                'required': 'Phone number is required',
            },
            'email': {
                'required': 'Email address is required',
                'invalid': 'Enter a valid email address',
            },
            'address_line_1': {
                'required': 'Primary address is required',
            },
            'country': {
                'required': 'Please select a country',
            },
            'state': {
                'required': 'Please provide a state',
            },
            'city': {
                'required': 'Please provide a city',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator(message="Enter a valid email address.")
            validator(email)
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.startswith('+') and not phone.startswith('0'):
                raise forms.ValidationError("Phone number must start with + or 0.")
            if len(phone) < 10:
                raise forms.ValidationError("Phone number is too short.")
        return phone
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
