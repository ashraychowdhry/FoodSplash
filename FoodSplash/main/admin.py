from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.FSUser)
class FSUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DropSite)
class DropSiteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Donation)
class DonationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Promise)
class PromiseAdmin(admin.ModelAdmin):
    pass

