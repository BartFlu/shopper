from django.shortcuts import HttpResponseRedirect, reverse, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, LoginForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def register(request):

    if request.user.is_authenticated:

        return HttpResponseRedirect(reverse('main'))

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email exists")
            user = form.save()
            user.set_password(user.password)
            user.save()

            return HttpResponseRedirect(reverse('login'))
        else:

            return render(request, 'Recipes/auth/register.html', context={'errors': form.errors})

    else:
        form = UserForm()
        context_dict = {'form': form}

        return render(request, 'Recipes/auth/register.html', context=context_dict)


def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            return HttpResponseRedirect(reverse('main'))
        else:

            return render(request, 'Recipes/auth/login.html', context={'errors': form.errors})

    else:

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))

        form = LoginForm()
        context = {'form': form}

        return render(request, 'Recipes/auth/login.html', context=context)


@login_required()
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('main'))