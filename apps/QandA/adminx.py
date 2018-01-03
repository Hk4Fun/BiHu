__author__ = 'Hk4Fun'
__date__ = '2017/12/27 0:23'

import xadmin
from .models import Tag, Question, Article, Comment


class TagAdmin(object):
    list_display = ['name', 'add_time']
    search_fields = ['name']
    list_filter = ['name', 'add_time']


class QuestionAdmin(object):
    list_display = ['title', 'desc', 'view_nums', 'asker',
                    'tags', 'concerned_users', 'likes', 'add_time']
    search_fields = ['title', 'desc', 'asker__username', 'tags__name', 'concerned_users__username']
    list_filter = ['title', 'desc', 'view_nums', 'asker__username',
                    'tags__name', 'concerned_users__username',  'add_time']
    readonly_fields = ['view_nums','likes']

class ArticleAdmin(object):
    list_display = ['view_nums', 'up_nums', 'down_nums', 'question', 'author', 'collected_users', 'likes', 'add_time']
    search_fields = ['content', 'question__title', 'author__username', 'question__tags__name']
    list_filter = ['view_nums', 'up_nums', 'down_nums', 'question__title', 'author__username', 'collected_users__username', 'add_time']
    readonly_fields = ['view_nums', 'up_nums', 'down_nums', 'likes']



class CommentAdmin(object):
    list_display = ['content', 'up_nums', 'down_nums', 'reviewer','add_time']
    search_fields = ['content', 'reviewer__username']
    list_filter = ['content', 'up_nums', 'down_nums', 'reviewer__username','add_time']
    readonly_fields = ['up_nums', 'down_nums',]


xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Comment, CommentAdmin)
