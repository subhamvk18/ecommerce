
from . import views
from django.urls import path

urlpatterns=[
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('signup',views.signup,name='signup'),
    path('check',views.check,name='check'),
    path('pascheck',views.pascheck,name='pascheck'),
    path('showproduct/<str:slug>',views.product,name='product'),#show product categorywise
    path('product/<str:slug>',views.showproduct,name='showproduct'),#show singlw product
    path('addcarts/<str:slug>',views.addcarts,name='addcarts'),
     path('removecarts/<str:slug>',views.removecarts,name='removecarts'),
    path('showcarts/<str:slug>',views.showcarts,name='showcarts'),
    path('increasecarts/<str:slug>',views.increasecarts,name='increasecarts'),
    path('decreasecarts/<str:slug>',views.decreasecarts,name='decreasecarts'),
    path('ordercart/<str:slug>',views.ordercart,name='ordercart'),
    path('search/<str:slug>',views.search,name='search'),#search page
    path('searchauto', views.get_places, name='get_places'),#autocomplete features serach input in base.html
    path('account/<str:slug>', views.account, name='account'),
    path('order/<str:slug>', views.order, name='order'),
    path('addingadd',views.adding,name='adding'),#adding address field
    path('placeaddress',views.placeaddress,name='placeaddress'),#slect address field
    path('showorder/<str:slug>',views.showorder,name='showorder'),#slect every order
    path('cancel/<str:slug>',views.cancelorder,name='showorder'),#cancel order

    path('orderhome',views.orderhome,name='orderhome'),
    path('showaddress/<str:slug>', views.showaddress, name='showaddress'),
    path('updateaddress/<str:slug>', views.updateaddress, name='updateaddress'),

    path('placeorder/<str:slug>', views.placeorder, name='placeorder'),

    path('removecart', views.removecart, name='removecart'),
    path('undercomplete/<str:slug>', views.undercomplete, name='undercomplete'),
    path('payment/<str:slug>', views.payment, name='payment'),

    path('deltaddress/<str:slug>', views.deltaddress, name='deltaddress'),
    path('changeuser/<str:slug>', views.changeuser, name='changeuser'),



]