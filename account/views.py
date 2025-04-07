from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from account.forms import LoginForm, RegistrationForm

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
                
                return redirect('login')
            else:
                form.add_error('password', 'Passwords do not match.')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)


    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate using email and password
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to a home page or dashboard
            else:
                form.add_error('password', 'Invalid email or password')  # Custom error for login failure
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)


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


def logout(request):
    return render(request, 'account/logout.html')