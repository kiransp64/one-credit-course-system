# core/forms.py
from django import forms
from .models import CustomUser
from .models import Quiz
from django.contrib.auth.forms import UserCreationForm
from .models import Question
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
import re
from .models import Choice

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'role', 'phone_number', 'branch', 'usn','profile_picture']
    
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    email = forms.EmailField(validators=[EmailValidator(message="Please enter a valid email address in the format: example@domain.com.")])
    phone_number = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must contain exactly 10 digits.')]
    )
    branch = forms.CharField(max_length=100, required=False)
    usn = forms.CharField(max_length=100, required=False)
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")

        if role == "teacher":
            self.fields['usn'].required = False
            self.fields['branch'].required = True
        elif role == "student":
            self.fields['branch'].required = False
            self.fields['usn'].required = True

        return cleaned_data

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Removed the length check, it's already handled by 'min_length=8'
        
        if not re.search(r"[A-Za-z]", password):  # Check for a mix of letters
            raise ValidationError("Your password must contain at least one letter.")
        
        if not re.search(r"\d", password):  # Check for a mix of numbers
            raise ValidationError("Your password must contain at least one number.")

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("The two password fields didn’t match.")
        
        return password2


class QuizUploadForm(forms.Form):
    excel_file = forms.FileField(label="Upload Excel File")




class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz')
        super(QuizForm, self).__init__(*args, **kwargs)
        
        for question in quiz.questions.all():
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=[(choice.choice_text, choice.choice_text) for choice in question.choices.all()],
                widget=forms.RadioSelect,
                label=question.question_text
            )


