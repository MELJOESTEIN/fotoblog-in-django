from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from . import forms
from django.contrib.auth.decorators import login_required

class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm
   

    def get(self, request):
        form = self.form_class()
        messages = ''
        return render(request, self.template_name, {'form': form, 'messages': messages})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages = f'Bonjour {user.username}! Vous avez bien été connecté.'
                return redirect('home')
            else:
                messages = 'Identifiant ou mot de passe incorrect.'
        
        return render(request, self.template_name, {'form': form})


class SignupPageView(View):
    form_class = forms.SignUpForm
    template_name = 'authentication/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': form})





@login_required
def logout_user(request):
    logout(request)
    return redirect('login')