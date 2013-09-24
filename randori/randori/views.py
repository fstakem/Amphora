from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.conf import settings
from django import forms


# Landing
def landing(request):
    data = { 'view': 'Home' } 
    return render_to_response('landing.html', data)

# Misc
def features(request):
    data = { 'view': 'Features' }
    return render_to_response('features.html', data)

def blog(request):
    data = { 'view': 'Blog' }
    return render_to_response('blog.html', data)

def terms(request):
    data = { 'view': 'Terms' }
    return render_to_response('terms.html', data)

def privacy(request):
    data = { 'view': 'Privacy' }
    return render_to_response('privacy.html', data)

def about(request):
    data = { 'view': 'About' }
    return render_to_response('about.html', data)

def contact(request):
    data = { 'view': 'Contact' }
    return render_to_response('contact.html', data)

# Authentication forms
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, 
                               label="Username")
    password = forms.CharField(widget=forms.PasswordInput, 
                               label="Password")

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        return user

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label="Username",
                                error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    first_name = forms.CharField(max_length=255, 
                                 label="First name")
    last_name = forms.CharField(max_length=255, 
                                label="Last name")
    email = forms.EmailField(label="E-mail")
    password_a = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password_b = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")

    def clean_username(self):
        return self.cleaned_data['username']
        # existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        # if existing.exists():
        #     raise forms.ValidationError(_("A user with that username already exists."))
        # else:
        #     return self.cleaned_data['username']

    def clean(self):
        if 'password_a' in self.cleaned_data and 'password_a' in self.cleaned_data:
            if self.cleaned_data['password_a'] != self.cleaned_data['password_b']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


# Authentication
def login(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect("/" + user.username)

    return render(request, 'login.html', {'login_form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def register(request):
    form = RegistrationForm(request.POST or None)
    if request.POST and form.is_valid:
        # Save the user to the db

        return HttpResponseRedirect("/")# Redirect to a success page.

    return render(request, 'register.html', {'registration_form': form})




