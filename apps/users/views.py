import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Count
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from pure_pagination import Paginator, PageNotAnInteger
from django.views.generic.base import View
from QandA.models import Question, Article
from .forms import ImageUploadForm
from .models import User, Follow, Message
from . import verify


# 重载authenticate，实现用户名/邮箱/手机登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 默认情况下objects用逗号分开查询是and组合，使用Q查询来支持or组合"|"
            # Q()对象可以结合关键字参数一起传递给查询函数，不过需要注意的是要将Q()对象放在关键字参数的前面
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        QandA = [article for article in Article.objects.all()] \
                + [question for question in Question.objects.all()]
        QandA = sorted(QandA, key=lambda x: x.add_time, reverse=True)
        for QorA in QandA:
            if isinstance(QorA, Article):
                QorA.type = 'a'
            else:
                QorA.type = 'q'

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(QandA, 2, request=request)
        QA = p.page(page)

        NewQues = Question.objects.all().order_by('-add_time')[:5]  # 最新提问
        MostLikes = Question.objects.annotate(likes=Count('concerned_users')).order_by('-likes')[:5]  # 最多关注
        MostReply = Question.objects.annotate(count=Count('articles')).order_by('-count')[:5]  # 最多回答
        return render(request, 'index.html', locals())


class LoginRegView(View):
    def get(self, request):
        return render(request, 'login_reg.html')

    def post(self, request):
        if len(request.POST) == 2:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            if username and password:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    request.user.pwd_input_wrong_times = 0  # 正确登录时清零错误次数
                    request.user.save()
                    return HttpResponse('{"status":"success"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"failed", "msg":"用户名或密码错误！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"用户名或密码错误！"}', content_type='application/json')
        elif len(request.POST) == 6:
            name = request.POST.get('username')
            nickname = request.POST.get('nickname')
            phone = request.POST.get('mobile')
            pwd = request.POST.get('password')
            pwd2 = request.POST.get('password2')
            sex = request.POST.get('sex')
            name_msg = verify.verify_username(name)
            phone_msg = verify.verify_phone(phone)
            pwd_msg = verify.verify_pwd(pwd, pwd2)
            msg = {**name_msg, **phone_msg, **pwd_msg}
            if msg['phone'] == '' and msg['name'] == '' and msg['pwd'] == '':
                user = User()
                user.username = name
                user.nickname = nickname
                user.mobile = phone
                user.password = make_password(pwd)
                user.gender = sex
                user.email = 'example@example.com'
                user.save()
            return HttpResponse(json.dumps(msg), content_type='application/json')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('user:login_reg'))


class HomeView(View):
    def get(self, request, uid):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login_reg'))
        user = User.objects.filter(id=int(uid))
        if user:
            user = user[0]
            return render(request, 'home.html', locals())

    def post(self, request, uid):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "redirect":"用户未登陆！"}', content_type='application/json')

        if request.user.pwd_input_wrong_times == 3:  # 修改密码错了3次直接退出并返回登录页面
            logout(request)
            return HttpResponse('{"status":"fail", "redirect":"修改次数过多！"}', content_type='application/json')
        self_desc = request.POST.get('self_description')
        if self_desc != request.user.self_description:
            request.user.self_description = self_desc
            request.user.save()

        nickname = request.POST.get('nickname')
        if nickname != request.user.nickname:
            request.user.nickname = nickname
            request.user.save()

        gender = request.POST.get('sex')
        if gender != request.user.gender:
            request.user.gender = gender
            request.user.save()

        oldPwd = request.POST.get('oldPwd')
        if oldPwd:
            if not check_password(oldPwd, request.user.password):
                request.user.pwd_input_wrong_times += 1
                request.user.save()
                return HttpResponse(
                    '{"status":"fail", "oldPwd":"旧密码错误！还剩%s次机会!"}' % (3 - request.user.pwd_input_wrong_times),
                    content_type='application/json')
            newPwd = request.POST.get('newPwd')
            if newPwd:
                if len(newPwd) < 6:
                    return HttpResponse('{"status":"fail", "newPwd":"密码长度小于6位！"}', content_type='application/json')
                request.user.password = make_password(request.POST.get('newPwd'))
                request.user.save()

        mobile = request.POST.get('mobile')
        if mobile != request.user.mobile:
            phone_msg = verify.verify_phone(mobile)
            if phone_msg['phone']:
                return HttpResponse('{"status":"fail", "phone":"%s"}' % (phone_msg['phone']),
                                    content_type='application/json')
            request.user.mobile = mobile
            request.user.save()

        email = request.POST.get('email')
        if email != request.user.email:
            email_msg = verify.verify_email(email)
            if email_msg['email']:
                return HttpResponse('{"status":"fail", "email":"%s"}' % (email_msg['email']),
                                    content_type='application/json')
            request.user.email = email
            request.user.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class ImageUploadView(View):
    def post(self, request):
        # 用户头像上传
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login_reg'))
        # 用户头像放在request的FILES字段中
        # instance=request.user 传递一个实例给这个model，这样直接赋值，相当于
        # request.user.image = image_from.cleaned_data['image']
        image_from = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_from.is_valid():
            # request.user.image = image_from.cleaned_data['image']
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class FollowView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('redirect')
        followerId = request.GET.get('follower_id')
        followeeId = request.GET.get('followee_id')
        followTip = request.GET.get('follow_tip')

        if followerId == str(request.user.id) and followeeId and followTip:
            if followerId == followeeId:  # 自己关注自己
                return HttpResponse('self')
            elif followTip == 'cancel':
                follow = Follow.objects.get(follower_id=int(
                    followerId), follow_id=int(followeeId))
                follow.delete()
                return HttpResponse('canceled')
            elif followTip == 'ok':
                follow = Follow(follower_id=int(followerId), follow_id=int(followeeId))
                follow.save()
                return HttpResponse('focused')


class MessageView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login_reg'))
        for message in Message.objects.filter(to_user=request.user.id):  # 将未读改为已读
            message.has_read = True
            message.save()
        message_list = Message.objects.filter(Q(from_user=request.user.id) | Q(
            to_user=request.user.id)).order_by('-add_time')
        return render(request, 'inbox.html', locals())

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('redirect')
        from_user_id = request.POST.get('from_user_id')
        to_user_id = request.POST.get('to_user_id')
        message_text = request.POST.get('message_text')

        if from_user_id == str(request.user.id) and to_user_id and message_text:
            to_user = User.objects.filter(id=int(to_user_id))
            if to_user:
                message = Message()
                message.from_user = request.user
                message.to_user = to_user[0]
                message.content = message_text
                message.save()
                return HttpResponse('ok')
        return HttpResponse('fail')
