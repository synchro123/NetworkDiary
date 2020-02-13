from  django.urls import  path
from django.views.generic import RedirectView

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('diary/', views.diary, name='diary'),
    path('timetable/', views.timetable, name='timetable'),
    path('notifications/', views.notifi, name='notifications'),

    path('register/', views.director_register_menu, name='register_menu'),
    path('register/create/', views.create_director_user, name='create_director_user'),

    path('login/', views.SiteLoginView.as_view(), name='login_page'),
    path('logout/', views.SiteLogOut.as_view(), name='logout'),

    path('news/<int:article>/', views.det, name='det'),
    path('news/<int:article>/leave_comment/', views.leave_comment, name='leave_comment'),
    path('news/', RedirectView.as_view(url='/', permanent=True)),

    path('profile/', views.profile, name='profile'),


    # for director
    path('news/edit/', views.edit_article_page, name='edit_article'),
    path('news/update/<int:id>', views.update_article_page, name='update_article'),
    path('news/delete/<int:id>', views.delete_article_page, name='delete_article'),

    path('school_setup/', views.school_setup, name='school_setup'),
    path('school_setup/add/', views.add_school, name='create_school'),
    path('school_setup/edit/', views.edit_school, name='edit_school'),


    path('school_setup/add_class/', views.add_school_class, name='create_class'),
    path('school_setup/edit_class/<int:id>', views.edit_school_class, name='redact_class'),
    path('school_setup/delete_class/<int:id>', views.delete_school_class, name='delete_class'),

    path('school_setup/add_classmate/<int:id>', views.add_classmate_to_class, name='add_classmate'),
    path('school_setup/edit_child/<int:id>', views.edit_child, name='redact_classmate'),
    path('school_setup/delete_child/<int:id>', views.delete_child, name='delete_classmate'),

    path('school_setup/add_teacher/', views.add_teacher, name='add_teacher'),
    path('school_setup/edit_teacher/<int:id>', views.edit_teacher, name='edit_teacher'),
    path('school_setup/delete_teacher/<int:id>', views.delete_teacher, name='delete_teacher'),

    path('school_setup/edit_timetable/<int:id>', views.edit_timetable, name='redact_timetable'),

    path('school_setup/add_subject/', views.add_subject, name='add_subject'),

    path('school_setup/edit_subject/<int:id>', views.edit_teacher, name='edit_subject'),
    path('school_setup/delete_subject/<int:id>', views.delete_teacher, name='delete_subject'),

    #path('school_setup/add_subject_to_day/<int:id>', views.add_subject_to_day, name='add_subject_to_day'),

    path('school_setup/edit_daysubject/<int:id>', views.edit_subject_in_day, name='edit_daysubject'),
]