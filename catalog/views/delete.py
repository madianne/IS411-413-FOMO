from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect

@view_function
def process_request(request, product:cmod.Product):

    product.status= 'I'
    product.save()
    return HttpResponseRedirect('/catalog/ProductList/')

