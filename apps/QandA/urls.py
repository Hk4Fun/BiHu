__author__ = 'Hk4Fun'
__date__ = '2017/12/26 18:32'


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ask/$', views.AskView.as_view(), name='ask'),
    url(r'^article/(?P<qid>\d+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^answer/(?P<qid>\d+)/$', views.AnswerView.as_view(), name='answer'),
    url(r'^media/(?P<dir_name>[^/]+)$', views.UploadEditorImageView.as_view(), name='upload'),
    url(r'^search/$', views.SearchView.as_view(), name='search')
]