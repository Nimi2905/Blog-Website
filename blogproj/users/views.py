from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm, UserRegisterForm
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully Created for {username} Login In Now!!!')
            return redirect('login1')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'forms': form})
    '''

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['password']
        cpass = request.POST['confirmpassword']

        cnt = 0
        if User.objects.filter(username=username):
            messages.error(request, username + ' is already exist!! Please try another one')
            cnt = 1

        if User.objects.filter(email=email):
            messages.error(request, email + '  is already taken !! Please try another one')
            cnt = 1

        if len(username) > 10:
            messages.error(request, 'Username should be of at most 10 character')
            cnt = 1

        if pass1 != cpass:
            messages.error(request, 'Passsword is not matching')
            cnt = 1

        if not username.isalnum():
            messages.error(request, 'Username should be alphanumeric')
            cnt = 1

        if cnt == 1:
            return redirect('register')

        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(request, 'You are successfully registered')

        return redirect('login1')

    return render(request, 'users/register.html')
    '''


def login1(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully login')
            return redirect('../')
        else:
            messages.error(request, 'Invalid credentials!!')
            return redirect('login1')

    return render(request, 'users/login.html')


def logout1(request):
    logout(request)
    messages.success(request, "You have logged out succesfully")
    return redirect('../')


@login_required(login_url='login1')
def profile(request):
    return render(request, 'users/profile.html',)


@login_required(login_url='login1')
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile_update.html', {'u_form': u_form, 'p_form': p_form})


