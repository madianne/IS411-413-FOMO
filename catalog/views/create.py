from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod


@view_function
def process_request(request):
    # render the form
    form = TestForm(request)
    product = cmod.Product.objects.filter(status = 'A')
    if form.is_valid():
        # work of the form
        return HttpResponseRedirect('/catalog/ProductList/')
    context = {
        'form': form,
        'product': product,
    }
    return request.dmp_render('create.html', context)


class TestForm(Formless):
    def init(self):
        self.fields['Category'] = forms.ChoiceField(choices=cmod.Product.TYPE_CHOICES, required=False)
        self.fields['Name'] = forms.CharField(label='Name', required=False)
        self.fields['Status'] = forms.ChoiceField(choices=cmod.Product.STATUS_CHOICES, required=False)
        self.fields['Price'] = forms.CharField(label='Price', required=False)
        self.fields['Quantity'] = forms.CharField(label='Price', required=False)
        self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger', required=False)
        self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity', required=False)
        self.fields['max_rental_days'] = forms.CharField(label='Max Rental Days', required=False)
        self.fields['description'] = forms.CharField(label='Description', required=False)
        self.fields['retire_date'] = forms.CharField(label='Retire Date', required=False)
        self.fields['pid'] = forms.CharField(label='Product ID', required=False)

    def clean_name(self):
        name = self.cleaned_data.get('Name')
        if name == '':
            raise forms.ValidationError('This field is required')
        return name

    def clean_status(self):
        Status = self.cleaned_data.get('Status')
        if Status == '':
            raise forms.ValidationError('This field is required')
        return Status

    def clean_category(self):
        Category = self.cleaned_data.get('Category')
        if Category == '':
            raise forms.ValidationError('This field is required')
        return Category

    def clean_price(self):
        # Get the price
        price = self.cleaned_data.get('Price')
        if price == '':
            raise forms.ValidationError('This field is required')
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if self.clean_category() == 'BulkProduct':
            if quantity == '':
                raise forms.ValidationError('This field is required')
        return quantity

    def clean_reorder_trigger(self):
        reorder_trigger = self.cleaned_data.get('reorder_trigger')
        if self.clean_category() == 'BulkProduct':
            if reorder_trigger == '':
                raise forms.ValidationError('This field is required')
        return reorder_trigger

    def clean_reorder_quantity(self):
        reorder_quantity = self.cleaned_data.get('reorder_quantity')
        if self.clean_category() == 'BulkProduct':
            if reorder_quantity == '':
                raise forms.ValidationError('This field is required')
        return reorder_quantity

    def clean_max_rental_days(self):
        max_rental_days = self.cleaned_data.get('max_rental_days')
        if self.clean_category() == 'RentalProduct':
            if max_rental_days == '':
                raise forms.ValidationError('This field is required')
        return max_rental_days

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description == '':
            raise forms.ValidationError('This field is required')
        return description

    def clean_pid(self):
        pid = self.cleaned_data.get('pid')
        if pid == '':
            raise forms.ValidationError('This field is required')
        return pid

    def commit(self):
        if self.clean_category() == 'IndividualProduct':
            p1 = cmod.IndividualProduct()
            p1.name = self.clean_name()
            p1.status = self.clean_status()
            p1.category = self.clean_category()
            p1.price = self.clean_price()
            p1.description = self.clean_description()
            p1.pid = self.clean_pid()
            p1.save()
        if self.clean_category() == 'BulkProduct':
            p1 = cmod.BulkProduct()
            p1.name = self.clean_name()
            p1.status = self.clean_status()
            p1.category = self.clean_category()
            p1.price = self.clean_price()
            p1.quantity = self.clean_quantity()
            p1.reorder_trigger = self.clean_reorder_trigger()
            p1.reorder_quantity = self.clean_reorder_quantity()
            p1.description = self.clean_description()
            p1.pid = self.clean_pid()
            p1.save()
        if self.clean_category() == 'RentalProduct':
            p1 = cmod.RentalProduct()
            p1.name = self.clean_name()
            p1.status = self.clean_status()
            p1.category = self.clean_category()
            p1.price = self.clean_price()
            p1.max_rental_days = self.max_rental_days()
            p1.description = self.clean_description()
            p1.pid = self.clean_pid()
            p1.save()
        return HttpResponseRedirect('/catalog/ProductList/')
