import re
import string

import pdfkit
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
# Create your views here.
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
import json

from ecommerce import settings
from home.models import Carts, Category, Contact, Items
from order.models import Address, Order

def home(request):
   
    list=Items.objects.filter()[0:3]
    con={'list':list}
    return render(request,'home.html',con)



def about(request):

    return render(request,'about.html',)


@csrf_exempt
def contact(request):
   if request.user.is_authenticated:
       if request.method=='POST':

        email=request.POST['email']
        text=request.POST['text']

        con=Contact(user=request.user,text=text)
        con.save()
        messages.success(request,"messages sends successfully")
        return HttpResponse("true")
       else:
           return render(request,'contact.html')
   else:
       messages.info(request,"You need to login first")
       return  redirect("/contact")


def login(request):
    if request.method=='POST':
        if request.method == 'POST':
            username = request.POST['uname']
            password = request.POST['pass']
            user = auth.authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)
                messages.success(request, 'You have successfully login')

                return redirect("/")
            else:
                messages.error(request, 'Invalid credantials')
                return redirect('/login')
    else:
        return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        email=request.POST['email']
        uname=request.POST['username']
        npass=request.POST['password']
        cpass=request.POST['cpassword']
        name = request.POST['name']
        lis=[]
        lis=name.split(" ")
        if len(lis)==1:
            lis.append("")
        list = User.objects.filter(email=email)
        li = User.objects.filter(username=uname)
        l = User.objects.filter(password=cpass)
        if len(list) > 0:
            messages.info(request, 'You have already Signup with this email')
            return redirect('/signup')
        elif cpass != npass:
            messages.error(request, 'please enter same password for confirmation')
            return redirect('/signup')
        elif len(uname)<=5 or re.match("[0-9]{1}[a-z A-Z]{1}",uname)==False:
            messages.error(request, 'Username length more tha 4 and username contains atleast one alphabate and one digit')
            return redirect('/signup')

        elif len(cpass) < 8:
            messages.error(request, 'Your Password length must be greater than 7')
            return redirect('/signup')

        elif cpass.isdigit() == True or cpass.isalpha() == True:
            messages.error(request, 'Your Password length must contains atleast one letter and one digit')
            return redirect('/signup')

        elif len(li) > 0:
            messages.error(request, 'Username already exists Enter another username')
            return redirect('/signup')

        elif len(l) > 0:
            messages.error(request, 'Password already exists Enter another Password')
            return redirect('/signup')
        user = User.objects.create_user(first_name=lis[0],last_name=lis[1],username=uname, email=email, password=cpass)
        try:
            text = render_to_string('email.html', {'val': name})
            hc=strip_tags(text)
            mail = EmailMultiAlternatives('Signup success email',
                                          '',
                                          settings.EMAIL_HOST_USER,
                                          [email],
                                          reply_to=[email])
            mail.attach_alternative(hc, 'text/html')

            mail.send()
        except Exception as e:
            messages.error(request,"Please Enter a valid mail")
            return redirect("/")
        user.save()
        messages.success(request,"Signup Successful")
        return redirect("/login")


    else:
        return render(request,'signup.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Successfully log out')
    return redirect("/")



def check(request):
    uname=request.GET['uname']
    li = User.objects.filter(username=uname)
    if len(uname)>4 and uname.isdigit()==False and uname.isalpha()==False:
        return HttpResponse("true")
    elif len(li) > 0:
        return HttpResponse("false")
    else:
        return HttpResponse("false")

def pascheck(request):
    passw = request.GET['pass']
    li = User.objects.filter(password=passw)
    if len(passw) >=8 and passw.isdigit() == False and passw.isalpha() == False:
        return HttpResponse("true")
    elif len(li) > 0:
        return HttpResponse("false")
    else:
    
        return HttpResponse("false")


def product(request,slug):   #show product categorywise

    cat=Category.objects.get(slug=slug)
    item = Items.objects.filter(category=cat)

    paginator = Paginator(item,9)
    page = request.GET.get('page')
    try:
        item = paginator.page(page)
    except PageNotAnInteger:
        item = paginator.page(1)
    except EmptyPage:
        item = paginator.page(paginator.num_pages)

    con={'rdict':item}

    return render(request,'product.html',con)

def showproduct(request,slug): #show a single product

    li=Items.objects.get(slug=slug)
    con={'item':li}
    return render(request,'showproduct.html',con)


def addcarts(request,slug):
    if request.user.is_authenticated:
        item=Items.objects.get(slug=slug)
        cart=Carts(user=request.user,cart=item,quantity=1)
        cart.save()
        messages.success(request,"Item is save in your cart")

        return HttpResponse("true")
    else:
        messages.error(request,"first need to login")
        return HttpResponse("false")
def removecarts(request,slug):
    item=Items.objects.filter(slug=slug).first()
    cart = Carts.objects.filter(user=request.user, cart=item)
    for i in cart:

        i.delete()
    messages.success(request,"Item is delete from the cart")

    return HttpResponse("true")    


def showcarts(request,slug):
    user=User.objects.get(username=slug)
    carts=Carts.objects.filter(user=user).order_by('-id')
    if len(carts)==0:
        messages.info(request,"No Carts in your list")
        

    sum=0
    for i in carts:
       sum=sum+((i.quantity)*i.cart.price)


    paginator = Paginator(carts,3)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)   

    con1 = {'sum':sum,'con':users}
    return render(request,'showcart.html',con1)


def decreasecarts(requset,slug):
    item = Items.objects.get(slug=slug)
    #user = User.objects.get(username=request.user)
    li=Carts.objects.filter(user=requset.user,cart=item).first()
    li.quantity=li.quantity-1
    if li.quantity==0:
        li.delete()
    else:

        li.save()
    return HttpResponse("true")


def increasecarts(request,slug):
    item = Items.objects.get(slug=slug)
    user = User.objects.get(username=request.user)
    li = Carts.objects.filter(user=request.user,cart=item).first()
    li.quantity = li.quantity + 1
    li.save()
    return HttpResponse("true")



def deforder(list, slug):
   if slug=="relevance":
       list.sort(key=lambda x: x.id, reverse=True)
   elif slug == "name":
       list.sort(key=lambda x: x.name)
   elif slug == "-name":
       list.sort(key=lambda x: x.name,reverse=True)
   elif slug=="price":
       list.sort(key=lambda x: x.price)
   elif slug == "-price":
       list.sort(key=lambda x: x.price,reverse=True)
   else:
       list.sort(key=lambda x: x.id, reverse=True)
   return list





def search(request,slug):

    value=request.POST.get('searchproduct')




    st=str(value)
    if len(st)!=0:
        value=""
        li=[]
        list=[]
        item=Items.objects.filter(Q(name__contains=value)|Q(brand__contains=value))
        for i in item:
            list.append(i)



        newlist=deforder(list,slug)
        paginator = Paginator(newlist,4)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)


        con={'item':users}

        return render(request,'search1.html',con)

    else:
        messages.error(request,"please Enter any query")
        return redirect(request.META['HTTP_REFERER'])



def get_places(request):
  if request.is_ajax():

    q = request.GET.get('term', '')

    places =Items.objects.filter(Q(name__contains=q)|Q(brand__contains=q))
    print(places)
    results = []
    for pl in places:
      place_json = {}
      place_json = pl.name+' '+pl.brand
      results.append(place_json)
    data = json.dumps(results)
    print(data)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)


def ordercart(request,slug):
    item=Items.objects.get(slug=slug)
    u=request.user
    cart=Carts.objects.filter(cart=item,user=u)
    if len(cart)>0:
        messages.success(request,"The Items already in cart,Order from your cart")
        return redirect(request.META['HTTP_REFERER'])
    else:
        cart=Carts(user=u,cart=item,quantity=1)
        cart.save()
        return redirect(f"/showcarts/{u.username}")


def order(request,slug):
  order=Order.objects.filter(user=request.user,iscomplete=True).order_by('-id')

  paginator = Paginator(order, 4)
  page = request.GET.get('page')
  try:
      order = paginator.page(page)
  except PageNotAnInteger:
      order = paginator.page(1)
  except EmptyPage:
      order= paginator.page(paginator.num_pages)
  con={'order':order}
  return render(request,'order.html',con)




def account(request,slug):
    return render(request,'personalaccount.html')





#Order part views

def adding(request):
    name = request.POST.get('naddress', '')
    city = request.POST.get('ncity', '')
    post = request.POST.get('npost', '')
    pin = request.POST.get('npin', '')
    houseno = request.POST.get('nhouseno', 'NA')
    dist = request.POST.get('ndist', '')
    street = request.POST.get('nstreet', 'NA')
    state = request.POST.get('nstate', '')
    add = Address(user=request.user, name=name, city=city, pin=pin, post=post, houseno=houseno, dist=dist,
                  street=street, state=state)
    add.save()
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



def showorder(request,slug):
    order=Order.objects.get(slug=slug)
    return  render(request,'showorder.html',{'order':order})


def cancelorder(request,slug):
    order = Order.objects.get(slug=slug)

    for i in order.cart.all():
        i.cart.quantity=i.cart.quantity+i.quantity
        i.cart.save()
    user=request.user;
    order.delete()
    messages.success(request,'Order is cancel successfully')
    return redirect(f"/order/{user}")


def showaddress(request, slug):
    list = []
    list = Address.objects.filter(user=request.user)

    if len(list) == 0:
        messages.error(request, "No address field")
        con = {'orderslug': slug}

        return render(request, 'order/showaddress.html', con)

    else:
        j = 1;
        for i in list:
            i.no = j;
            i.save()
            j = j + 1;
        con = {'list': list, 'orderslug': slug}

        return render(request, 'order/showaddress.html', con)


def orderhome(request):
    cart = Carts.objects.filter(user=request.user)
    sum = 0
    for i in cart:
        if i.quantity > i.cart.quantity:
            messages.error(request, f"{i.cart.name} have only {i.cart.quantity} items")
            return redirect(request.META['HTTP_REFERER'])
    for i in cart:
        sum = sum + (i.quantity) * (i.cart.price)

    ob = Order(user=request.user, cost=sum, email=request.user.email, mobile="123456")
    ob.save()
    for i in cart:
        ob.cart.add(i)
    return redirect(f"/showaddress/{ob.slug}")


def placeorder(request, slug):
    order = Order.objects.get(slug=slug)
    if order.address == '':
        messages.info(request, 'Select any address')
        return redirect(request.META['HTTP_REFERER'])
    else:
        user = request.user;
        order = Order.objects.get(slug=slug)
        address = order.address
        li = address.split("\n")
        rdict = {}
        list = []
        for i in li:
            st = i.split("=")
            rdict[st[0]] = st[1]
        list = order.cart.all()
        sum = 0
        for i in list:
            sum = sum + (i.quantity) * i.cart.price
        con = {'rdict': rdict, 'user': user, 'cart': list, 'sum': sum, 'slug': slug}

        return render(request, 'order/placeorder.html', con)


def updateaddress(request, slug):
    add = Address.objects.get(slug=slug)
    name = request.POST.get('address', '')
    city = request.POST.get('city', '')
    post = request.POST.get('post', '')
    pin = request.POST.get('pin', '')
    houseno = request.POST.get('houseno', '')
    dist = request.POST.get('dist', '')
    street = request.POST.get('street', '')
    state = request.POST.get('state', '')
    add.name = name
    add.city = city
    add.dist = dist
    add.street = street
    add.state = state
    add.pin = pin
    add.post = post
    add.houseno = houseno
    add.save()
    messages.success(request, "Adddress update successfully")
    return redirect(request.META['HTTP_REFERER'])


def placeaddress(request):
    oslug = request.GET.get("orderslug")
    aslug = request.GET.get("addressslug")
    order1 = Order.objects.get(slug=oslug)
    address = Address.objects.filter(slug=aslug).first()
    add = f"village={address.name}\nstreetno={address.street}\nhouseno={address.houseno}\ndist={address.dist}\ncity={address.city}\nstate={address.state}\npost={address.post}\npin={address.pin}"
    order1.address = add
    order1.save()
    return HttpResponse("true")


def removecart(request):
    cid = request.GET.get('cid')
    oslug = request.GET.get('oslug')
    cart = Carts.objects.get(id=cid)
    order = Order.objects.get(slug=oslug)
    order.cart.remove(cart)
    order = Order.objects.get(slug=oslug)
    sum = 0
    for i in order.cart.all():
        sum = sum + (i.quantity) * (i.cart.price)
    order.cost = sum
    order.save()
    return HttpResponse("true")


def undercomplete(request, slug):
    order = Order.objects.get(slug=slug)
    email = request.GET.get('email')
    phone = request.GET.get('phone')

    order.email = email
    order.mobile = phone
    order.save()
    return HttpResponse("true")


def payment(request, slug):#last step
    order = Order.objects.get(slug=slug)
    if order.cost==0:
        order.delete()
        messages.error(request,"You have not select any item,Order is automatically cancel")
        return redirect(f"/showcarts/{request.user}")
    order.status = 'complete'
    order.iscomplete = True
    cart = order.cart.all()
    for i in cart:
        i.cart.quantity = i.cart.quantity - i.quantity
        i.cart.save()
    order.save()
    name=order.user.username
    try:
        text = render_to_string('completemail.html', {'val': name})
        hc = strip_tags(text)
        mail = EmailMultiAlternatives('Completion of Order',
                                      '',
                                      settings.EMAIL_HOST_USER,
                                      [order.email],
                                      reply_to=[order.email])
        mail.attach_alternative(hc, 'text/html')

        mail.send()
    except Exception as e:
        messages.error(request, "Please Enter a valid mail")
        return redirect("/")
    con = {'slug': slug}
    return render(request, 'order/completeorder.html', con)


def deltaddress(request, slug):
    add = Address.objects.get(slug=slug)
    add.delete()
    messages.success(request, "Address Delete Successfully")
    return redirect(request.META['HTTP_REFERER'])









def changeuser(request,slug): #change userdetails
    if request.method == 'POST':
        user = request.user
        name = request.POST['newname']
        email = request.POST['newemail']
        uname = request.POST['newusername']
        new = request.POST['new']

        li = User.objects.get(id=new)
        oldname = li.first_name + " " + li.last_name
        if email != li.email:
            li.email = email
        if uname != li.username:
            li.username = uname
        if oldname != name:
            st = name.split(' ')
            li.first_name = st[0]
            li.last_name = st[1]

        li.save()
        messages.success(request, 'Details update sucessfully')

        return redirect(request.META['HTTP_REFERER'])



