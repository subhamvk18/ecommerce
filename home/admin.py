from django.contrib import admin

from home.models import Contact, Items, Category, Carts, Comment, Cupon, Usecupon

# Register your models here.
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(Carts)
admin.site.register(Comment)
admin.site.register(Cupon)
admin.site.register(Usecupon)
