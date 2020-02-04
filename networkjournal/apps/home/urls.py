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
    path('school_setup/add_class/', views.add_school_class, name='create_school_class'),
    path('school_setup/delete_class/<int:id>', views.delete_school_class, name='delete_class'),
    path('school_setup/redact_class/<int:id>', views.redact_school_class, name='redact_class'),
    path('school_setup/add_classmate/<int:id>', views.add_classmate_to_class, name='add_classmate'),
    path('school_setup/delete_child/<int:id>', views.delete_child, name='delete_classmate'),
]