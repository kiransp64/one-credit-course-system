# core/admin.py
from django.contrib import admin
from .models import CustomUser, Quiz, Question, StudentPerformance, Attendance

admin.site.register(CustomUser)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(StudentPerformance)
admin.site.register(Attendance)
