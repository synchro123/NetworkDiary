import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from .user_fields import *

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

    teacher = models.IntegerField('ID классного руководителя')

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

class Timetable(models.Model):
    schoolClass = models.ForeignKey(Class, on_delete=models.CASCADE)

class DayOfWeek(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    dayname = models.CharField('Имя дня', max_length=50)

    def __str__(self):
        return self.dayname

class TimetableSchoolSubject(models.Model):
    dayofweek = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE)
    sublocalid = models.IntegerField('Порядковый номер урока')
    subjSourceId = models.IntegerField('ID школьного предмета')
    teacher = models.IntegerField('ID учителя')
    timeOfStart = models.TimeField('Время начала')
    timeOfEnd = models.TimeField('Время конца')

    def get_subject_model(self):
        return SchoolSubject.objects.get(pk=self.subjSourceId)

    def get_teacher_model(self):
        return User.objects.get(pk=self.teacher)

    def get_teacher_name_and_surname(self):
        return get_user_name(User.objects.get(pk=self.teacher)) + ' ' + get_user_surname(User.objects.get(pk=self.teacher))

    def get_teacher_name_and_surname_brackets(self):
        return '('+get_user_name(User.objects.get(pk=self.teacher)) + ' ' + get_user_surname(User.objects.get(pk=self.teacher))+')'

    def __str__(self):
        return SchoolSubject.objects.get(pk=self.subjSourceId).subj_name

class Mark(models.Model):
    schoolsubject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)

    mark_value = models.IntegerField('Номинал отметки')

    weekid = models.IntegerField('ID недели в году')

    usrid = models.IntegerField('ID пользователя(ученика)')

    date = models.DateField('data polycheniya')

    def __str__(self):
        return  str(self.mark_value)

class Homework(models.Model):
    schoolClass = models.ForeignKey(Class, on_delete = models.CASCADE)
    subject_id = models.IntegerField('id предмета')
    hwtitle = models.TextField('Название задания')
    hwtext = models.TextField('Текст задания')
    hw_deadline = models.DateField('deadline')
    hw_start = models.DateField('startline')

    def __str__ (self):
        return self.hwtext

    def is_actual(self):
        return  self.hw_deadline >= datetime.date.today() - datetime.timedelta(days=2)

