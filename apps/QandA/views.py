import json, re
from django.shortcuts import render
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from .models import Tag, Question, Article, Comment
from .handler import image_upload
import datetime


class AskView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"failed"}', content_type='application/json')
        question = Question()
        question.title = request.POST['question_name']
        question.desc = request.POST['question_description']
        question.asker = request.user
        question.save()
        tags = re.split(r' |,|\.|;|\*', request.POST['question_tag'])
        for tag in tags:
            tg = Tag.objects.filter(name=tag)
            if not tg:
                tg = Tag(name=tag)
                tg.save()
                question.tags.add(tg)
            else:
                question.tags.add(tg[0])
        return HttpResponse('{"status":"success"}', content_type='application/json')


class ArticleView(View):
    def get(self, request, qid):
        question = Question.objects.filter(id=int(qid))
        if question:
            question = question[0]
            question.view_nums += 1
            question.save()
            # 相关问题
            tags = Question.objects.get(id=int(qid)).tags.all()
            questions = []
            for tag in tags:
                for que in tag.question_set.filter(~Q(id=question.id)):
                    questions.append(que)

            return render(request, 'article_detail.html', locals())


class AnswerView(View):
    def get(self, request, qid):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login_reg'))
        question = Question.objects.filter(id=int(qid))
        if question:
            question = question[0]
            article = question.articles.filter(author_id=request.user.id)
            if article:
                article = article[0]
            return render(request, 'answer.html', locals())

    def post(self, request, qid):
        article_content = request.POST['article_content']
        question = Question.objects.filter(id=int(qid))
        if question:
            question = question[0]
            article = question.articles.filter(author_id=request.user.id)
            if article:
                article = article[0]
                article.content = article_content
                article.add_time = datetime.datetime.now()  # 更新文章时间
                article.save()
            else:
                art = Article()
                art.content = article_content
                art.question = question
                art.author = request.user
                art.save()
                question.articles.add(art)
            return HttpResponse('{"status":"success"}', content_type='application/json')


class UploadEditorImageView(View):
    def post(self, request, dir_name):
        ##################
        #  kindeditor图片上传返回数据格式说明：
        # {"error": 1, "message": "出错信息"}
        # {"error": 0, "url": "图片地址"}
        ##################
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login_reg'))
        result = {"error": 1, "message": "上传出错！"}
        files = request.FILES.get("imgFile", None)
        if files:
            result = image_upload(files, dir_name)
        return HttpResponse(json.dumps(result), content_type="text/html")


class SearchView(View):
    def get(self, request):
        searchText = request.GET.get('searchText', default='')
        if searchText:
            Qlist = Question.objects.filter(
                Q(title__contains=searchText) |
                Q(tags__name__contains=searchText)) \
                .distinct().annotate(likes=Count('concerned_users')).order_by('-likes')
            # 分页
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(Qlist, 2, request=request)
            questions = p.page(page)

            NewQues = Question.objects.all().order_by('-add_time')[:5]  # 最新提问
            MostLikes = Question.objects.annotate(likes=Count('concerned_users')).order_by('-likes')[:5]  # 最多关注
            MostReply = Question.objects.annotate(count=Count('articles')).order_by('-count')[:5]  # 最多回答
            return render(request, 'search.html', locals())


class CommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('redirect')
        comment_content = request.POST.get('comment_content', '')
        article_id = request.POST.get('article_id', '')
        if comment_content and article_id:
            comment = Comment()
            comment.reviewer = request.user
            comment.content = comment_content
            comment.article = Article.objects.get(id=article_id)
            comment.save()
            return HttpResponse('ok')


class ThumbUpView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('redirect')
        article_id = request.POST.get('article_id', '')
        comment_id = request.POST.get('comment_id', '')
        action = request.POST.get('action', '')
        if article_id and action:  # 给文章点赞或取消赞
            articles = Article.objects.filter(id=article_id)
            if articles:
                if action == 'ok':
                    articles[0].up_nums += 1
                    articles[0].save()
                    return HttpResponse('success')
                elif action == 'cancel':
                    articles[0].up_nums -= 1
                    articles[0].save()
                    return HttpResponse('success')
        elif comment_id and action:  # 给评论点赞获取消赞
            comments = Comment.objects.filter(id=comment_id)
            if comments:
                if action == 'ok':
                    comments[0].up_nums += 1
                    comments[0].save()
                    return HttpResponse('success')
                elif action == 'cancel':
                    comments[0].up_nums -= 1
                    comments[0].save()
                    return HttpResponse('success')

        return HttpResponse('fail')


class ThumbDownView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('redirect')


class QuestionConcernedView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('redirect')
        user_id = request.POST.get('user_id')
        question_id = request.POST.get('question_id')
        action = request.POST.get('action')

        if user_id == str(request.user.id) and question_id and action:
            question = Question.objects.filter(id=question_id)
            if question:
                question = question[0]
                if action == 'cancel': # 取消关注
                    question.concerned_users.remove(request.user)
                    question.save()
                    return HttpResponse('canceled')
                elif action == 'ok':  # 关注
                    question.concerned_users.add(request.user)
                    question.save()
                    return HttpResponse('focused')
        return HttpResponse('fail')