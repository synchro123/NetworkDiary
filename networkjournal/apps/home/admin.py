from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(School)
admin.site.register(Class)

admin.site.register(SchoolSubject)
admin.site.register(DayOfWeek)
admin.site.register(TimetableSchoolSubject)
admin.site.register(Timetable)
admin.site.register(Homework)
admin.site.register(Mark)