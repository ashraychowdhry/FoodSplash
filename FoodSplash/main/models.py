from django.db import models
from FoodSplash.settings import PRODUCTION
from django.contrib.auth.models import User

# Load User model based on environment
if PRODUCTION:
    from djangae.contrib.gauth_datastore.models import GaeDatastoreUser
    User = GaeDatastoreUser

# Create your models here.


class Address(models.Model):
    street = models.CharField(null=True, max_length=250)
    city = models.CharField(null=True, max_length=100)
    state = models.CharField(null=True, max_length=100)
    zip = models.CharField(null=True, max_length=50)

    def __str__(self):
        return "{}, {}, {} {}".format(self.street, self.city, self.state, self.zip)


class FSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email


class DropSite(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    notes = models.TextField(null=True)
    email = models.EmailField()

    def __str__(self):
        return str(self.address)


class Donation(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    drop_site = models.ForeignKey(DropSite)
    fs_user = models.ForeignKey(FSUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=1)


class Promise(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    drop_site = models.ForeignKey(DropSite)
    fs_user = models.ForeignKey(FSUser, on_delete=models.CASCADE)

