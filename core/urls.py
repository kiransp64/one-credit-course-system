# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile_dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('quiz/<str:course_id>/', views.take_quiz, name='take_quiz'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_dashboard, name='profile_dashboard'),

]
