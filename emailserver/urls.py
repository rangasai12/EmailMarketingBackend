from django.urls import path

from . import views


urlpatterns =[
    path('',views.home, name = "home"),
    path('add-subscriber/', views.add_subscriber, name='add-subscriber'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]