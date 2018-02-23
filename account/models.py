from django.db import models
from cuser.models import AbstractCUser

# Create your models here.
class User(AbstractCUser):
    birthdate = models.DateTimeField(null=True)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zipcode = models.TextField(null=True, blank=True)

    def get_purchases(self):
        return['roku', 'skis', 'Computer']
