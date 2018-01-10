__author__ = 'Hk4Fun'
__date__ = '2018/1/8 1:28'

from django import template
from QandA.models import Question
from users.models import Follow
import time, datetime

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
    dt = datetime.datetime.fromtimestamp(t)
    return '%s年%s月%s日' % (dt.year, dt.month, dt.day)

@register.filter()
def my_follows(uid):  # 获取关注的人
    return [fol.follow  for fol in Follow.objects.filter(follower=uid)]

@register.filter()
def my_followers(uid):  # 获取关注我的人
    return [fol.follower for fol in Follow.objects.filter(follow=uid)]