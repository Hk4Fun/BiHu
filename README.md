# BiHu--[在线演示](http://bihu.hk4fun.tk)

使用 Django 仿照知乎实现的问答社交平台，前端使用 Bootstrap3 和 Ajax，后台管理使用 xadmin，数据库使用 Django ORM 自带的 Sqlite3 引擎

## 当前功能

- 多用户登陆注册，用户之间可互相私信和关注
- 浏览他人或自己的个人主页，修改自己的个人信息，如头像上传修改等
- 主页分页展示最新动态和热门排行
- 用户可对感兴趣的问题进行关注，也可对文章进行点赞和评论
- 对问题进行标签化处理，用户可通过标签搜索相关问题

## 安装启动

```
git clone https://github.com/Hk4Fun/BiHu.git
```

```
cd BiHu
```

```
pip install pipenv
```

```
pipenv install
```

```
pipenv shell
```

```
python manage.py migrate
```

```
python manage.py runserver
```

