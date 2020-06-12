

from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from home.models import Carts
from order.models import Address, Order




def showaddress(request,slug):

    list = []
    list=Address.objects.filter(user=request.user)

    if len(list)==0:
        messages.error(request,"No address field")
        con = {'orderslug': slug}
        
        return render(request,'order/showaddress.html',con)

    else:
        j=1;
        for i in list:
            i.no=j;
            i.save()
            j=j+1;
        con={'list':list,'orderslug':slug}


        return render(request,'order/showaddress.html',con)

def orderhome(request):
    cart = Carts.objects.filter(user=request.user)
    sum = 0
    for i in cart:
        if i.quantity>i.cart.quantity:
            messages.error(request,f"{i.cart.name} have only {i.cart.quantity} items")
            return redirect(request.META['HTTP_REFERER'])
    for i in cart:
        sum = sum + (i.quantity) * (i.cart.price)

    ob = Order(user=request.user, cost=sum, email=request.user.email,mobile="123456")
    ob.save()
    for i in cart:
        ob.cart.add(i)
    return redirect(f"/order/showaddress/{ob.slug}")





def placeorder(request,slug):
    order=Order.objects.get(slug=slug)
    if order.address=='':
        messages.info(request,'Select any address')
        return redirect(request.META['HTTP_REFERER'])
    else:
        user=request.user;
        order=Order.objects.get(slug=slug)
        address=order.address
        li=address.split("\n")
        rdict={}
        list=[]
        for i in li:
            st=i.split("=")
            rdict[st[0]]=st[1]
        list=order.cart.all()
        sum=0
        for i in list:
            sum=sum+(i.quantity)*i.cart.price
        con={'rdict':rdict,'user':user,'cart':list,'sum':sum,'slug':slug}

        return render(request,'order/placeorder.html',con)




def updateaddress(request,slug):
    add=Address.objects.get(slug=slug)
    name=request.POST.get('address','')
    city=request.POST.get('city','')
    post=request.POST.get('post','')
    pin=request.POST.get('pin','')
    houseno=request.POST.get('houseno','')
    dist=request.POST.get('dist','')
    street=request.POST.get('street','')
    state=request.POST.get('state','')
    add.name=name
    add.city=city
    add.dist=dist
    add.street=street
    add.state=state
    add.pin=pin
    add.post=post
    add.houseno=houseno
    add.save()
    messages.success(request,"Adddress update successfully")
    return redirect(request.META['HTTP_REFERER'])

def placeaddress(request):

    oslug=request.GET.get("orderslug")
    aslug=request.GET.get("addressslug")
    order1=Order.objects.get(slug=oslug)
    address=Address.objects.filter(slug=aslug).first()
    add=f"village={address.name}\nstreetno={address.street}\nhouseno={address.houseno}\ndist={address.dist}\ncity={address.city}\nstate={address.state}\npost={address.post}\npin={address.pin}"
    order1.address=add
    order1.save()
    return HttpResponse("true")


def removecart(request):

    cid=request.GET.get('cid')
    oslug=request.GET.get('oslug')
    cart=Carts.objects.get(id=cid)
    order=Order.objects.get(slug=oslug)
    order.cart.remove(cart)
    order = Order.objects.get(slug=oslug)
    sum=0
    for i in order.cart.all():
        sum=sum+(i.quantity)*(i.cart.price)
    order.cost=sum
    order.save()
    return HttpResponse("true")


def undercomplete(request,slug):
    order=Order.objects.get(slug=slug)
    email=request.GET.get('email')
    phone=request.GET.get('phone')

    order.email=email
    order.mobile=phone
    order.save()
    return HttpResponse("true")


def payment(request,slug):
    order=Order.objects.get(slug=slug)
    order.status='complete'
    order.iscomplete=True
    cart=order.cart.all()
    for i in cart:
        i.cart.quantity=i.cart.quantity-i.quantity
        i.cart.save()
    order.save()
    con={'slug':slug}
    return render(request,'order/completeorder.html',con)









def deltaddress(request,slug):
    add=Address.objects.get(slug=slug)
    add.delete()
    messages.success(request,"Address Delete Successfully")
    return redirect(request.META['HTTP_REFERER'])