from django.contrib.auth import authenticate, login, logout
from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Permission, Group, ContentType

class UserTestCases(TestCase):
   # def setUp(self):
      #  Animal.objects.create(name="lion", sound="roar")
       # Animal.objects.create(name="cat", sound="meow")
    fixtures = ['users.yaml']

    def test_load_save(self):
        '''test creating, saving, and reloading a user'''
        u1 = amod.User()
        u1.first_name = 'lisa'
        u1.last_name = 'simpson'
        u1.email = 'lisa@simpsons.com'
        '''hash the password'''
        u1.set_password('password')
        '''save the person'''
        u1.save()
        '''pull user back out'''
        u2 = amod.User.objects.get(email = 'lisa@simpsons.com')
        self.assertEqual(u1.first_name, u2.first_name)
        self.assertEqual(u1.last_name, u2.last_name)
        self.assertEqual(u1.email, u2.email)
        self.assertTrue(u2.check_password('password'))


    def test_groups_adding_groups(self):
        '''testing a few groups'''
        u1 = amod.User()
        u1.first_name = 'lisa'
        u1.last_name = 'simpson'
        u1.email = 'lisa@simpsons.com'
        '''hash the password'''
        u1.set_password('password')
        '''save the person'''
        u1.save()
        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()
        u1.groups.add(g1)
        u1.save()
        self.assertTrue(u1.groups.filter(name = 'Salespeople').exists())

    def test_password(self):
       '''testing password hashing'''
       u1 = amod.User()
       u1.set_password('password')
       u1.save()
       self.assertTrue(u1.check_password('password'))
       u1.save()


    def test_add_permissions(self):
       '''testing a few groups'''
       u1 = amod.User()
       '''save the person'''
       u1.save()
       permission = Permission.objects.get(
        codename='change_product_price',
        content_type=1,)
       u1.user_permissions.add(permission)
       self.assertTrue(u1.has_perm('change_product_price'))

    def test_field_changes(self):
       '''test field changes'''
       self.u1 = amod.User()
       self.u1.first_name = 'lisa'
       self.u1.last_name = 'simpson'
       self.u1.email = 'lisa@simpsons.com'
       '''hash the password'''
       self.u1.set_password('password')
       '''save the person'''
       self.u1.save()
       u2 = amod.User.objects.get(email = 'lisa@simpsons.com')
       self.assertEqual(self.u1.first_name, u2.first_name)
       self.assertEqual(self.u1.last_name, u2.last_name)
       self.assertEqual(self.u1.email, u2.email)
       self.assertTrue(u2.check_password('password'))


