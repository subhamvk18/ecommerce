from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.utils.timezone import now

from ecommerce.utils import unique_slug_generator
from home.models import Items, Carts





class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    no=models.IntegerField(default=0)
    name=models.CharField(max_length=300)
    street=models.CharField(max_length=200,null=True,blank=True,default="NA")
    houseno=models.CharField(max_length=200,null=True,blank=True,default="NA")
    city = models.CharField(max_length=200,default='')
    dist = models.CharField(max_length=200,default='')
    state= models.CharField(max_length=200,default='')
    post=models.CharField(max_length=200)
    pin=models.CharField(max_length=200)
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    stime=models.DateTimeField(default=now)
    etime=models.DateTimeField(default=now)
    cart=models.ManyToManyField(Carts)
    address=models.TextField(max_length=1000,default='')
    cost=models.IntegerField()
    email=models.EmailField(default='')
    mobile=models.CharField(max_length=10,default='')
    ispayment=models.BooleanField(default=False)
    iscomplete=models.BooleanField(default=False)
    status=models.CharField(max_length=100,default="initiate")
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)



    def __str__(self):
        return "order of "+self.user.username


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:

        instance.slug =unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender=Order)
pre_save.connect(pre_save_receiver, sender=Address)