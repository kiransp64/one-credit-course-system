from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views  # Import views from the core app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),  # Homepage URL
    path('register/', views.register, name='register'),  # Registration URL
    path('login/', views.login_view, name='login'),  # Login URL
    path('core/', include('core.urls')),
    path('send-email/', views.send_email_to_student, name='send_email'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
