from django.core.management.base import BaseCommand
from core.models import CustomUser, Quiz
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send reminder emails to students about upcoming quizzes'

    def handle(self, *args, **kwargs):
        # Get all quizzes that are scheduled within the next 24 hours
        upcoming_quizzes = Quiz.objects.filter(upload_date__gte=timezone.now(), upload_date__lt=timezone.now() + timedelta(days=1))

        for quiz in upcoming_quizzes:
            students = CustomUser.objects.filter(role='student')  # Get all students
            for student in students:
                # Sending the reminder email
                subject = f"Reminder: Upcoming Quiz on {quiz.course_id}"
                message = f"Dear {student.username},\n\nThis is a reminder that the quiz for the course {quiz.course_id} is scheduled to take place soon. Please make sure to attend it.\n\nBest regards,\nYour Team"
                from_email = 'your_email@gmail.com'  # Your email address
                recipient_list = [student.email]

                send_mail(subject, message, from_email, recipient_list)

        self.stdout.write(self.style.SUCCESS('Successfully sent reminder emails!'))
