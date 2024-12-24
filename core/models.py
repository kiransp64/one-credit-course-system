from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Enter a valid phone number.")
    branch = models.CharField(max_length=100, blank=True, null=True, help_text="Branch (Only for Teachers)")
    usn = models.CharField(max_length=15, blank=True, null=True, help_text="University Serial Number (Only for Students)")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Quiz(models.Model):
    course_id = models.CharField(max_length=50)
    question = models.TextField(help_text="Main question text")
    correct_answer = models.TextField(help_text="Correct answer for the question")
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True, help_text="Optional image for the quiz")
    upload_date = models.DateField(auto_now_add=True)
    deadline = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=1), help_text="Deadline for the quiz")

    def __str__(self):
        return f"Quiz: {self.course_id} (Deadline: {self.deadline})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, help_text="The text of the question")
    correct_answer = models.CharField(max_length=100, help_text="Correct answer text")

    def __str__(self):
        return f"Question: {self.question_text} (Quiz: {self.quiz.course_id})"


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255, help_text="Answer choice text")
    is_correct = models.BooleanField(default=False, help_text="Mark if this is the correct choice")

    def __str__(self):
        return f"Choice: {self.choice_text} ({'Correct' if self.is_correct else 'Incorrect'})"


class Attendance(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, help_text="Student or teacher user")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, help_text="Quiz the user attended")
    is_attended = models.BooleanField(default=False, help_text="Mark if the quiz was attended")

    def __str__(self):
        return f"{self.user} {'attended' if self.is_attended else 'missed'} {self.quiz.course_id}"


class StudentPerformance(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, help_text="Student who took the quiz")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, help_text="Quiz the student attempted")
    score = models.IntegerField(help_text="Score obtained by the student")
    date_taken = models.DateField(auto_now_add=True, help_text="Date when the quiz was taken")

    def __str__(self):
        return f"{self.student.username} - {self.quiz.course_id}: {self.score} points"
