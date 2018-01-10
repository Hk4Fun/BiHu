from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, default="", verbose_name="昵称", )
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别")
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="地址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    image = models.ImageField(upload_to="user/image/%Y/%m/%d", default="user/image/default.jpg", verbose_name="头像")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    self_description = models.CharField(max_length=128, default='我什么都没写', verbose_name='一句话介绍')
    pwd_input_wrong_times = models.IntegerField(default=0, verbose_name='修改密码错误次数')
    # follow = models.ManyToManyField('self', through='Follow', symmetrical=False, verbose_name='关注')
    # send_message = models.ManyToManyField('self', through='Message', symmetrical=False, verbose_name='发私信')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followers', verbose_name='关注者')
    follow = models.ForeignKey(User, related_name='follows', verbose_name='关注了')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        unique_together = (("follower", "follow"),)

    def __str__(self):
        return self.follower.username + ' follows ' + self.follow.username


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='from_users', verbose_name='发信人')
    to_user = models.ForeignKey(User, related_name='to_users', verbose_name='收信人')
    content = models.TextField(verbose_name='私信内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发信时间')

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'from ' + self.from_user.username + ' to ' + self.to_user.username

