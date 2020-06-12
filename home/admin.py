from django.contrib import admin

from home.models import Contact, Items, Category, Carts

# Register your models here.
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(Carts)
