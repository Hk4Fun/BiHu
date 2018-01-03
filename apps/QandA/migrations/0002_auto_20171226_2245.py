# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-26 22:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('QandA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='asker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='askers', to=settings.AUTH_USER_MODEL, verbose_name='提问者'),
        ),
        migrations.AddField(
            model_name='question',
            name='concerned_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='被关注者'),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='QandA.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='QandA.Article', verbose_name='文章'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to=settings.AUTH_USER_MODEL, verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='article',
            name='collected_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='被收藏者'),
        ),
        migrations.AddField(
            model_name='article',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='QandA.Question', verbose_name='问题'),
        ),
    ]
