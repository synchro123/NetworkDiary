import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class School(models.Model):
    director = models.CharField('username директора', max_length=50)
    name = models.CharField('имя школы', max_length=50)

    site = models.URLField('Сайт', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'школа'
        verbose_name_plural = 'школы'

class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    num = models.IntegerField('Цифра класса')
    letter = models.CharField('Буква класса', max_length=1)

    def __str__(self):
        return str(self.num) + '\"' + self.letter + '\"'

    class Meta:
        verbose_name = 'школьный класс'
        verbose_name_plural = 'школьные классы'

class Article(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField('Название статьи', max_length=200)
    text = models.TextField('Текст статьи')
    date = models.DateTimeField('Дата написания', auto_now=True)

    def __str__(self):
        return self.title

    def was_pub_recently(self):
        return self.date >= (timezone.now() - datetime.timedelta(days=7))

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Comment(models.Model):
    test = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField('Автор', max_length=50)
    text = models.CharField('Текст', max_length=200)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

class SchoolSubject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    subj_name = models.CharField('Название предмета', max_length=100)

    def __str__(self):
        return self.subj_name

    class Meta:
        verbose_name = 'школьный предмет'
        verbose_name_plural = 'школьные предметы'