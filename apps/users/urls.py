__author__ = 'Hk4Fun'
__date__ = '2017/12/26 18:32'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login_reg/$', views.LoginRegView.as_view(), name='login_reg'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^home/(?P<uid>\d+)/$', views.HomeView.as_view(), name='home'),
    url(r'^image/upload/$', views.ImageUploadView.as_view(), name='image_upload'),  # 用户头像上传
    url(r'^follow/$', views.FollowView.as_view(), name='follow') # 用户关注或取消关注
]