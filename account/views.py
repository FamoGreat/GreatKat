from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as django_logout
from account.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator

from account.models import Account


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        confirm_password = request.POST.get('confirm_password')
        
        if form.is_valid():
            if form.cleaned_data['password'] == confirm_password:
                user = form.save(commit=False)
                
                # Extract email and set username
                email = form.cleaned_data['email']
                username = email.split('@')[0]
                user.username = username
                
                # Set password and save user
                user.set_password(form.cleaned_data['password'])
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Please activate your account.'
                message = render_to_string('account/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMultiAlternatives(
                        subject=mail_subject,
                        body=message,
                        to=[to_email]       
                    )
                email.attach_alternative(message, "text/html")
                email.send()
                return render(request, 'account/verify_email.html')

            else:
                form.add_error('password', 'Passwords do not match.')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate the user with the email (since email is the username)
            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)  # Log the user in
                return redirect('home')  # Redirect to the home page after successful login
            else:
                form.add_error(None, 'Invalid email or password')  # Add error if authentication fails

    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)


@login_required(login_url='login') 
def logout(request):
    django_logout(request)  
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save() 
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')
    

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'account/dashboard.html')
    else:
        return redirect('home') 



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('account/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email = EmailMultiAlternatives(
                    subject=mail_subject,
                    body=message,
                    to=[to_email]       
                )
            email.attach_alternative(message, "text/html")
            email.send()
            messages.success(request, 'Password reset link has been sent to your email.')
        except Account.DoesNotExist:
            messages.error(request, 'Email not found.')

    return render(request, 'account/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password.")
        return redirect('reset_password')
    else:
        messages.error(request, "This link is invalid or has expired.")
        return redirect('forgot_password')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'account/reset_password.html')

 
