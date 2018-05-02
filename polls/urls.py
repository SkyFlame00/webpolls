from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logoutView, name='logout'),
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('myprofile/edit/', views.myprofile_edit, name='myprofile_edit'),
    path('testing', views.testing, name='testing')
]
