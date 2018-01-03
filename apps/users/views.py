import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, PageNotAnInteger
from django.views.generic.base import View
from QandA.models import Question
from .models import User
from . import verify


class IndexView(View):
    def get(self, request):
        searchText = request.GET.get('searchText', default='')

        if searchText:
            Qlist = Question.objects.filter(
                Q(title__contains=searchText) | Q(tags__name__contains=searchText)).distinct().order_by('-likes')
        else:
            Qlist = Question.objects.all().order_by('-likes')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(Qlist, 5, request=request)
        q_list = p.page(page)

        return render(request, 'index.html', locals())


class LoginRegView(View):
    def get(self, request):
        return render(request, 'login_reg.html')

    def post(self, request):
        if len(request.POST) == 2:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponse('{"status":"success"}', content_type='application/json')
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
