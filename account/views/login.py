from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, RedirectException
from formlib import Formless
from django import forms
from account import models as amod


@view_function
def process_request(request):
    # render the form
    form = MyForm(request)
    if form.is_valid():
        # work of the form
        form.commit()
        raise RedirectException('/account/')

    return request.dmp_render('login.html', { 'form': form })

class MyForm(Formless):
    def init(self):
        self.fields['email'] = forms.EmailField(label='Email Address')
        self.fields['Password'] = forms.CharField(label='Password', widget=forms.PasswordInput)
        self.user = None

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('Password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')
        return self.cleaned_data

    def commit(self):
        login(self.request, self.user)
