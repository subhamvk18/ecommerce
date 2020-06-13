from django import template
from django.contrib.auth.models import User

from home.models import Carts, Items, Category
from order.models import Order

register = template.Library()
#custom filter of products.html


@register.filter(name='find')
def subtract(value):
    return value.keys()


@register.filter(name='findvalue')
def subtract(value,rdict):
    return rdict[value]


#customfilter of base.html
@register.filter(name='findcart')
def findcart(value):
    user=User.objects.get(username=value)
    cart=Carts.objects.filter(user=user)
    li=[]
    cartli=[]
    for i in cart:
        if i.cart.slug not in li:
            cartli.append(i)
            li.append(i.cart.slug)
    n=len(cartli)
    return n

@register.filter(name="findcategory")
def findcategory(value):
    li=Category.objects.filter()

    return li

#customfilter of showproduct.html

@register.filter(name='checkcart')
def checkcart(value,slug):

    user=User.objects.get(username=value)
    item=Items.objects.get(slug=slug)
    cart=Carts.objects.filter(user=user,cart=item)
    n=len(cart)
    print(n)
    if len(cart)>0:
        return "true"
    else:
        return "false"


#customfilter of showcart.html
@register.filter(name='findproduct')
def checkcart(value,slug):

    user=User.objects.get(username=value)
    item=Items.objects.get(slug=slug)
    cart=Carts.objects.get(user=user,cart=item)
    n=cart.quantity


    return n
@register.filter(name='totalprice')
def totalprice(value,user):
    cart=Carts.objects.filter(cart=value,user=user)
    c=cart[0]

    n=(c.quantity)*c.cart.price
    return n

@register.filter(name="tp")
def tp(value,arg):
    return value*arg


#personalaccount.html

@register.filter(name="cart")
def tp(value):
    order=Carts.objects.filter(user=value)
    n=len(order)
    return n


@register.filter(name="order")
def tp(value):
    order = Order.objects.filter(user=value,iscomplete=True)
    n = len(order)
    return n
