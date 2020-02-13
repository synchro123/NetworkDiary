from django.core.checks import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import *
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AuthUserForm, ArticleForm

from .user_fields import *

from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('home:login_page'))
    else:
        if get_user_status(request.user) == '0': return HttpResponseRedirect('/admin/')

        try:
            sc = School.objects.get(id=get_user_school(request.user))
        #a = Article.objects.get(school=sc).order_by('-date')
        except:
            return HttpResponseRedirect(reverse('home:school_setup'))
        a = sc.article_set.order_by('-date')
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        if get_user_status(request.user) == 'director':
            return render(request, 'director/list.html', {'article': a, 'username': username})
        elif get_user_status(request.user) == 'teacher':
            return render(request, 'teacher/list.html', {'article': a, 'username': username})
        else:
            return render(request, 'child/list.html', {'article': a, 'username': username})


def profile(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('home:login_page'))
    else:
        if get_user_status(request.user) == '0': return HttpResponseRedirect('/admin/')
        profile = request.user
        r_username = get_user_name(request.user)
        r_usersurname = get_user_surname(request.user)
        r_userfathername = get_user_fathername(request.user)
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        if get_user_status(request.user) == 'director':
            r_userrole = 'директор / системный администратор'
            return render(request, 'director/profile.html',
                          {'profile': profile, 'username': username, 'role': r_userrole, 'name': r_username,
                           'surname': r_usersurname, 'fathername': r_userfathername})
        else:
            r_userrole = 'ученик'
            return render(request, 'child/profile.html',
                          {'profile': profile, 'username': username, 'role': r_userrole, 'name': r_username,
                           'surname': r_usersurname, 'fathername': r_userfathername})


def notifi(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('home:login_page'))
    else:
        if get_user_status(request.user) == '0': return HttpResponseRedirect('/admin/')
        a = Article.objects.order_by('-date')[:5]
        # return render(request, 'home/notifi.html', {'notifications': a})
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        if get_user_status(request.user) == 'director':
            return render(request, 'director/notifi.html', {'username': username})
        else:
            return render(request, 'child/notifi.html', {'username': username})


def timetable(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('home:login_page'))
    else:
        if get_user_status(request.user) == '0': return HttpResponseRedirect('/admin/')
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        return render(request, 'child/timetable.html', {'username': username})


def det(request, article):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('home:login_page'))
    else:
        if get_user_status(request.user) == '0': return HttpResponseRedirect('/admin/')
        try:
            a = Article.objects.get(id=article)
        except:
            raise Http404('Такой статьи не существует')

        latest_comm_list = a.comment_set.order_by('-id')[:10]
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)

        if get_user_status(request.user) == 'director':
            return render(request, 'director/det.html',
                          {'article': a, 'latest_comm_list': latest_comm_list, 'username': username})
        elif get_user_status(request.user) == 'teacher':
            return render(request, 'teacher/det.html',
                          {'article': a, 'latest_comm_list': latest_comm_list, 'username': username})
        else:
            return render(request, 'child/det.html',
                          {'article': a, 'latest_comm_list': latest_comm_list, 'username': username})


def leave_comment(request, article):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('home:login_page'))
    else:
        if get_user_status(request.user) == '0': return HttpResponseRedirect('/admin/')
        try:
            a = Article.objects.get(id=article)
        except:
            raise Http404('Такой статьи не существует')

        a.comment_set.create(author=get_user_name(request.user) + ' ' + get_user_surname(request.user),
                             text=request.POST['text'])

        return HttpResponseRedirect(reverse('home:det', args=(a.id,)))


def director_register_menu(request):
    return render(request, 'register/director_register.html')


def create_director_user(request):
    userName = request.POST['userName']

    userRealName = request.POST['userRealName']
    userLastName = request.POST['userLastName']
    userFatherName = request.POST['userFatherName']

    userEmail = request.POST['inputEmail']

    userPassword = request.POST['inputPassword']
    userPasswordReq = request.POST['inputPasswordReq']
    if userPassword == userPasswordReq:
        newUser = User.objects.create_user(userName, userEmail, userPassword)
        newUser.last_name = 'director___' + userRealName + '___' + userLastName + '___' + userFatherName + '___schoolid=0'
        newUser.save()
        return HttpResponseRedirect(reverse('home:login_page'))


def edit_article_page(request):
    if get_user_status(request.user) == '0': return HttpResponseRedirect('/admin/')
    if get_user_status(request.user) == 'director':
        success = False
        try:
            sc = School.objects.get(director=request.user)
        except:
            return HttpResponseRedirect(reverse('home:school_setup'))
        if request.method == 'POST':
            title = request.POST['title']
            text = request.POST['text']
            sc.article_set.create(title=title, text=text)
            sc.save()
            return HttpResponseRedirect(reverse('home:edit_article'))

        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        template = 'director/edit_page.html'
        context = {
            'list_articles': sc.article_set.all(),
            'username': username,
            'success': success
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('home:edit_article'))


def update_article_page(request, id):
    if get_user_status(request.user) == 'director':
        a = Article.objects.get(pk=id)
        if request.method == 'POST':
            title = request.POST['title']
            text = request.POST['text']
            a.title = title
            a.text = text
            a.save()
            return HttpResponseRedirect(reverse('home:edit_article'))

        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        template = 'director/edit_page.html'
        context = {
            'get_article': a,
            'update': True,
            'username': username,
            'req_title': a.title,
            'req_text': a.text
        }

        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('home:edit_article'))


def delete_article_page(request, id):
    a = Article.objects.get(pk=id)
    a.delete()
    return HttpResponseRedirect(reverse('home:edit_article'))

class SiteLoginView(LoginView):
    template_name = 'user_login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home:index')

    def get_success_url(self):
        return self.success_url


class SiteLogOut(LogoutView):
    next_page = reverse_lazy('home:login_page')


def diary(request):
    if get_user_status(request.user) == 'child':
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        return render(request, 'child/diary.html', {'username': username})
    else:
        return HttpResponseRedirect(reverse('home:index'))


def school_setup(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:login_page'))
    if get_user_status(request.user) == 'director':
        try:
            a = School.objects.get(director=request.user)
        except:
            return HttpResponseRedirect(reverse('home:create_school'))
        classes = a.class_set.order_by('id')
        users_list = User.objects.all()
        users_teachers_info = []
        for u in users_list:
            if (get_user_status(u) == 'teacher' and get_user_school(u) == str(a.id)):
                fio = get_user_name(u)[0] + '. ' + get_user_fathername(u)[0] + '. ' + get_user_surname(u)
                users_teachers_info.append([u, fio])

        subjects = a.schoolsubject_set.all()
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        template = 'director/school_setup.html'
        context = {
            'username': username,
            'school': a,
            'classes': classes,
            'teachers': users_teachers_info,
            'subjects': subjects
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('home:index'))


def add_school(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:login_page'))
    if get_user_status(request.user) == 'director':
        try:
            a = School.objects.get(director=request.user)
        except:
            if request.method == 'POST':
                sc_name = request.POST['sc_name']
                sc = School(director=request.user, name=sc_name)
                sc.save()
                set_user_school(request.user, sc.id)
                request.user.save()
                return HttpResponseRedirect(reverse('home:school_setup'))
            username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
            template = 'director/school_setup.html'
            context = {
                'username': username,
            }
            return render(request, template, context)
        return HttpResponseRedirect(reverse('home:school_setup'))
    else:
        return HttpResponseRedirect(reverse('home:index'))

def edit_school(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:login_page'))
    if get_user_status(request.user) == 'director':
        sc = School.objects.get(pk=get_user_school(request.user))
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        template = 'director/edit_school_main.html'
        context = {
            'username': username,
            'req_name': sc.name,
            'req_site': sc.site
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('home:index'))

def add_school_class(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:login_page'))
    if get_user_status(request.user) == 'director':
        try:
            a = School.objects.get(director=request.user)
        except:
            return HttpResponseRedirect(reverse('home:school_setup'))
        if request.method == 'POST':
            cl_num = request.POST['cl_num']
            cl_char = request.POST['cl_letter']
            cl = a.class_set.create(num=int(cl_num), letter=cl_char)
            cl.save()
            return HttpResponseRedirect(reverse('home:school_setup'))
        username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
        template = 'director/school_setup.html'
        context = {
            'username': username,
            'addclass': True
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('home:index'))


def delete_school_class(request, id):
    a = Class.objects.get(pk=id)
    a.delete()
    return HttpResponseRedirect(reverse('home:school_setup'))


def edit_school_class(request, id):
    a = Class.objects.get(pk=id)
    if request.method == 'POST':
        cl_num = request.POST['cl_num']
        cl_char = request.POST['cl_letter']
        a.num = int(cl_num)
        a.letter = cl_char
        a.save()

    users_list = User.objects.all()
    users_inclass_info = []
    for u in users_list:
        if(int(get_user_class(u)) == id):
            fio = get_user_name(u)[0]+'. '+get_user_fathername(u)[0]+'. '+get_user_surname(u)
            users_inclass_info.append([u, fio])

    username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
    template = 'director/school_setup.html'
    context = {
        'username': username,
        'editclass': True,
        'req_num': a.num,
        'req_char': a.letter,
        'classid': id,
        'classmates': users_inclass_info,
    }
    return render(request, template, context)

def add_classmate_to_class(request, id):
    a = Class.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        fathername = request.POST['fathername']

        usrname = request.POST['username']
        pwd = request.POST['password']

        newUser = User.objects.create_user(usrname, '', pwd)
        newUser.last_name = 'child___' + name + '___' + surname + '___' + fathername + '___schoolid=' + get_user_school(request.user) + '___classid=' + str(id)
        newUser.save()
        return HttpResponseRedirect('/school_setup/edit_class/'+str(id))
    username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
    template = 'director/school_setup.html'
    context = {
        'username': username,
        'editclass': True,
        'addclassmate': True,
    }
    return render(request, template, context)

def delete_child(request, id):
    a = User.objects.get(pk=id)
    clid = get_user_class(a)
    a.delete()
    return  HttpResponseRedirect('/school_setup/edit_class/'+str(clid))

def edit_child(request, id):
    a = User.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        fathername = request.POST['fathername']

        a.last_name = 'child___' + name + '___' + surname + '___' + fathername + '___schoolid=' + get_user_school(a) + '___classid=' + str(get_user_class(a))
        a.save()
        return HttpResponseRedirect('/school_setup/edit_class/'+str(get_user_class(a)))

    template = "director/edit_child.html"
    username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
    context = {
        'username': username,
        'mname': get_user_name(a),
        'sname': get_user_surname(a),
        'fname': get_user_fathername(a),
    }
    return render(request, template, context)

def add_teacher(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        fathername = request.POST['fathername']

        usrname = request.POST['username']
        pwd = request.POST['password']

        newUser = User.objects.create_user(usrname, '', pwd)
        newUser.last_name = 'teacher___' + name + '___' + surname + '___' + fathername + '___schoolid=' + get_user_school(request.user)
        newUser.save()
        return HttpResponseRedirect('/school_setup/')
    template = 'register/teacher_register.html'
    context = {

    }
    return render(request, template, context)

def delete_teacher(request, id):
    a = User.objects.get(pk=id)
    a.delete()
    return HttpResponseRedirect('/school_setup/')

def edit_teacher(request, id):
    a = User.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        fathername = request.POST['fathername']

        a.last_name = 'teacher___' + name + '___' + surname + '___' + fathername + '___schoolid=' + get_user_school(a)
        a.save()
        a_class = get_user_class(a)
        return HttpResponseRedirect('/school_setup/')

    template = "director/edit_teacher.html"
    username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
    context = {
        'username': username,
        'mname': get_user_name(a),
        'sname': get_user_surname(a),
        'fname': get_user_fathername(a),
    }
    return render(request, template, context)

def add_subject(request):

    if request.method == 'POST':
        sc = School.objects.get(director=request.user)
        nm = request.POST['m_name']
        new_subject = sc.schoolsubject_set.create(subj_name= nm)
        return HttpResponseRedirect('/school_setup/')

    template = "director/add_subject.html"
    username = get_user_name(request.user) + ' ' + get_user_surname(request.user)
    context = {
        'username': username,
    }
    return render(request, template, context)

def edit_timetable(request, id):
    if get_user_status(request.user) != 'director':
        return HttpResponseRedirect('/')
    else:
        try:
            class_ = Class.objects.get(pk=id)
        except:
            return HttpResponseRedirect('/school_setup/')

        try:
            ttable = class_.timetable_set.get(schoolClass=class_)
        except:
            ttable = class_.timetable_set.create(schoolClass=class_)

        #get days
        try:
            monday = ttable.dayofweek_set.get(dayname='Понедельник')
        except:
            ttable.dayofweek_set.create(dayname='Понедельник')

        try:
            tuesday = ttable.dayofweek_set.get(dayname='Вторник')
        except:
            ttable.dayofweek_set.create(dayname='Вторник')

        try:
            wednesday = ttable.dayofweek_set.get(dayname='Среда')
        except:
            ttable.dayofweek_set.create(dayname='Среда')

        try:
            thurthday = ttable.dayofweek_set.get(dayname='Четверг')
        except:
            ttable.dayofweek_set.create(dayname='Четверг')

        try:
            friday = ttable.dayofweek_set.get(dayname='Пятница')
        except:
            ttable.dayofweek_set.create(dayname='Пятница')

        try:
            saturday = ttable.dayofweek_set.get(dayname='Суббота')
        except:
            ttable.dayofweek_set.create(dayname='Суббота')
        #end get days

        #add subjects
        c = 1
        while c <= 8:
            try:
                m1 = monday.timetableschoolsubject_set.get(sublocalid=c)
            except:
                m1 = monday.timetableschoolsubject_set.create(sublocalid=c, subjSourceId=1, teacher=0,
                                                              timeOfStart=timezone.now(), timeOfEnd=timezone.now())
            c += 1
        c = 1
        while c <= 8:
            try:
                m1 = tuesday.timetableschoolsubject_set.get(sublocalid=c)
            except:
                m1 = tuesday.timetableschoolsubject_set.create(sublocalid=c, subjSourceId=1, teacher=0,
                                                              timeOfStart=timezone.now(), timeOfEnd=timezone.now())
            c += 1
        c = 1
        while c <= 8:
            try:
                m1 = wednesday.timetableschoolsubject_set.get(sublocalid=c)
            except:
                m1 = wednesday.timetableschoolsubject_set.create(sublocalid=c, subjSourceId=1, teacher=0,
                                                              timeOfStart=timezone.now(), timeOfEnd=timezone.now())
            c += 1
        c = 1
        while c <= 8:
            try:
                m1 = thurthday.timetableschoolsubject_set.get(sublocalid=c)
            except:
                m1 = thurthday.timetableschoolsubject_set.create(sublocalid=c, subjSourceId=1, teacher=0,
                                                              timeOfStart=timezone.now(), timeOfEnd=timezone.now())
            c += 1
        c = 1
        while c <= 8:
            try:
                m1 = friday.timetableschoolsubject_set.get(sublocalid=c)
            except:
                m1 = friday.timetableschoolsubject_set.create(sublocalid=c, subjSourceId=1, teacher=0,
                                                              timeOfStart=timezone.now(), timeOfEnd=timezone.now())
            c += 1
        c = 1
        while c <= 8:
            try:
                m1 = saturday.timetableschoolsubject_set.get(sublocalid=c)
            except:
                m1 = saturday.timetableschoolsubject_set.create(sublocalid=c, subjSourceId=1, teacher=0,
                                                              timeOfStart=timezone.now(), timeOfEnd=timezone.now())
            c += 1
        #end add subjects

        #get subjects
        monday_ = monday.timetableschoolsubject_set.all()
        tuesday_ = tuesday.timetableschoolsubject_set.all()
        wednesday_ = wednesday.timetableschoolsubject_set.all()
        thurthday_ = thurthday.timetableschoolsubject_set.all()
        friday_ = friday.timetableschoolsubject_set.all()
        saturday_ = saturday.timetableschoolsubject_set.all()
        #end get subjects

        template = 'director/timetable.html'
        context = {
            'days': [[monday, monday_], [tuesday, tuesday_], [wednesday, wednesday_], [thurthday, thurthday_], [friday, friday_], [saturday, saturday_]]
        }
        return render(request, template, context)

def edit_subject_in_day(request, id):

    if request.method == 'POST':
        subject =

    template = 'director/edit_subject_in_day.html'
    users_list = User.objects.all()
    teachers_list = []
    for user in users_list:
        try:
            if get_user_school(user) == get_user_school(request.user) and get_user_status(user) == 'teacher':
                teachers_list.append(user)
        except:
            pass

    context = {
        'subjects': School.objects.get(director=request.user).schoolsubject_set.all(),
        'teachers': teachers_list
    }
    return render(request, template, context)
