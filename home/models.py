from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils.timezone import now




# Create your models here.
from ecommerce.utils import unique_slug_generator


class Contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(max_length=500)
    time=models.DateTimeField(default=now)



class Category(models.Model):
    catlist=[('Books','books'),('Masks','mask'),('Santizers','sanitizers'),('Icecreams','icecreams')]
    name=models.CharField(max_length=200,choices=catlist)
    slug=models.SlugField(max_length=50,null=True,blank=True);
    cimg=models.ImageField(upload_to='pics',null=True)

    def __str__(self):
        return self.name;


class Items(models.Model):
    name=models.CharField(max_length=200)
    brand=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField();
    image=models.ImageField(upload_to='pics',null=True)
    price=models.IntegerField()
    quantity=models.IntegerField(default=0)
    slug=models.SlugField(max_length=100,null=True,blank=True);

    def __str__(self):
        return self.name




def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug =unique_slug_generator(instance)
class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(Items,on_delete=models.CASCADE)
    time=models.DateTimeField(default=now)
    quantity=models.IntegerField(default=0)


pre_save.connect(pre_save_receiver, sender=Items)
pre_save.connect(pre_save_receiver, sender=Category)
