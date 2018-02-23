from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account import models as amod


@view_function
def process_request(request):
    # render the form
    form = TestForm(request)
    if form.is_valid():
        # work of the form

        return HttpResponseRedirect('/')

    context = {
        'form': form,
    }
    return request.dmp_render('signup.html', context)


class TestForm(Formless):
    def init(self):
        self.fields['Email'] = forms.EmailField(label='Email')
        self.fields['Password'] = forms.CharField(label='Password', widget=forms.PasswordInput)
        self.fields['Password2'] = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
        self.fields['Address'] = forms.CharField(label='Address')

    def clean_password(self):
        password = self.cleaned_data.get('Password')
        password2 = self.cleaned_data.get('Password2')
        if len(password) < 8:
            raise forms.ValidationError('Password must be 8 characters long')
        if any(i.isdigit() for i in password) == True:
            raise forms.ValidationError('Password must contain a number')
        return password

    def clean(self):
        password1 = self.cleaned_data.get('Password')
        password2 = self.cleaned_data.get('Password2')
        if password2 != password1:
            raise Exception('Please ensure passwords match')
        return self.cleaned_data

    def clean_Address(self):
        Address = self.cleaned_data.get('Address')
        return Address

    def clean_email(self):
        email = self.cleaned_data.get('Email')
        return email


    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = self.objects.get(email=email)
        except self.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    def commit(self):
        u1 = amod.User()
        u1.email = self.clean_email()
        u1.set_password = self.clean_password()
        u1.address = self.clean_Address()
        u1.save()
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.Password.cleaned_data.get('Password'))
        login(self.request, self.user)
        return self.cleaned_data


