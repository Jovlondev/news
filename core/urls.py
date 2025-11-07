from django.urls import path
from .views import *
from .auth_views import auth



urlpatterns = [
    path('',index,name='home'),
    path('category/<slug>/',ctg,name='ctg'),
    path('view/<int:pk>/',view,name='view'),
    path('srch/',search,name='search'),
    path('contact/',cnt,name='contact'),

    path('add_to_subs/<path>/',add_to_subs,name='subs_add'),

    # login + register
    path('auth/',auth,name='auth'),
    # path('logout/',auth,name='logout')


]