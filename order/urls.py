from django.urls import path

from order import views

urlpatterns=[
    path('',views.orderhome,name='orderhome'),
    path('showaddress/<str:slug>',views.showaddress,name='showaddress'),
    path('updateaddress/<str:slug>',views.updateaddress,name='updateaddress'),

    path('placeorder/<str:slug>',views.placeorder,name='placeorder'),

    path('removecart',views.removecart,name='removecart'),
    path('undercomplete/<str:slug>',views.undercomplete,name='undercomplete'),
    path('payment/<str:slug>',views.payment,name='payment'),

    path('deltaddress/<str:slug>',views.deltaddress,name='deltaddress'),
]