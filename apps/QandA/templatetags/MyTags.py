__author__ = 'Hk4Fun'
__date__ = '2018/1/8 1:28'

from django import template
from QandA.models import Question
from users.models import Follow, Message
import time

register = template.Library()


@register.simple_tag()
def get_question_likes(qid):
    return Question.objects.get(id=int(qid)).likes()


@register.filter()
def since(t):
    delta = int(time.time() - time.mktime(t.timetuple()))
    if delta < 60:
        return '1分钟前'
    if delta < 3600:
        return '%s分钟前' % (delta // 60)
    if delta < 86400:
        return '%s小时前' % (delta // 3600)
    if delta < 604800:
        return '%s天前' % (delta // 86400)

    return '%s年%s月%s日' % (t.year, t.month, t.day)

@register.filter()
def my_follows(uid):  # 获取关注的人
    return [fol.follow  for fol in Follow.objects.filter(follower=uid)]

@register.filter()
def my_followers(uid):  # 获取关注我的人
    return [fol.follower for fol in Follow.objects.filter(follow=uid)]

@register.simple_tag() # 获取用户未读消息数量
def unread_message_num(uid):
    return Message.objects.filter(to_user=uid, has_read=False).count()