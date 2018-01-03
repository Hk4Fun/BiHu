__author__ = 'Hk4Fun'
__date__ = '2017/12/26 18:32'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login_reg/$', views.LoginRegView.as_view(), name='login_reg'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

]