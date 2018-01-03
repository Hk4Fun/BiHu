__author__ = 'Hk4Fun'
__date__ = '2017/12/27 0:23'

import xadmin
from xadmin import views
from .models import Follow, Message


class BaseSetting(object):
    enable_themes = True   # 开启主题设置
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "逼乎后台管理系统"
    site_footer = "逼乎"
    menu_style = "accordion"  # 手风琴--使左侧的菜单目录可以收放

class FollowAdmin(object):
    list_display = ['follower', 'follow', 'add_time']
    search_fields = ['follower__username', 'follow__username']
    list_filter = ['follower__username', 'follow__username', 'add_time']

class MessageAdmin(object):
    list_display = ['from_user', 'to_user', 'content', 'add_time']
    search_fields = ['from_user__username', 'to_user__username', 'content']
    list_filter = ['from_user__username', 'to_user__username', 'content', 'add_time']

xadmin.site.register(Follow, FollowAdmin)
xadmin.site.register(Message, MessageAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)     # 注册xadmin基础设置
xadmin.site.register(views.CommAdminView, GlobalSettings)  # 注册xadmin全局设置
