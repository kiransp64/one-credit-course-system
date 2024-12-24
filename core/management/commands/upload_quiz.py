from django.core.management.base import BaseCommand
from core.models import Quiz, Question, Choice  # Adjust based on your app's structure
from django.utils import timezone

class Command(BaseCommand):
    help = 'Uploads quiz data on a weekly basis'

    def handle(self, *args, **kwargs):
        # Example of adding a quiz for weekly uploads
        quiz = Quiz.objects.create(
            course_id="Course-101",  # Example course ID
            upload_date=timezone.now()
        )

        # Example of adding questions to the quiz
        question1 = Question.objects.create(
            quiz=quiz,
            question_text="What is 2+3?",
            correct_answer="5"
        )

        # Example of adding choices to the question
        Choice.objects.create(
            question=question1,
            choice_text="3"
        )
        Choice.objects.create(
            question=question1,
            choice_text="4"
        )
        Choice.objects.create(
            question=question1,
            choice_text="5"
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded quiz for {quiz.course_id}!'))
