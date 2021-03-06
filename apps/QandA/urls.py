__author__ = 'Hk4Fun'
__date__ = '2017/12/26 18:32'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ask/$', views.AskView.as_view(), name='ask'),
    url(r'^article/(?P<qid>\d+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^answer/(?P<qid>\d+)/$', views.AnswerView.as_view(), name='answer'),
    url(r'^media/(?P<dir_name>[^/]+)$', views.UploadEditorImageView.as_view(), name='upload'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^comment/$', views.CommentView.as_view(), name='comment'),
    url(r'^thumbUp/$', views.ThumbUpView.as_view(), name='thumbUp'),  # 用户点赞和取消赞
    url(r'^thumbDown/$', views.ThumbDownView.as_view(), name='thumbDown'), # 用户踩和取消踩
    url(r'^question_concerned/$', views.QuestionConcernedView.as_view(), name='question_concerned'), # 用户关注和取消关注问题
]
