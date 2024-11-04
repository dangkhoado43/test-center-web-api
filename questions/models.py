from django.db import models
from users.models import CustomUser
from authors.models import Author
from tests.models import Test


class QuestionCategory(models.Model):
    name = models.CharField(max_length=200, blank=False)
    
    class Meta:
        db_table = 'question_categories'

    def __str__(self):
        return self.name

class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('multiple_choice', 'Multiple Choice'),
        ('single_choice', 'Single Choice'),
        ('text', 'Text'),
        ('essay', 'Essay'),
        ('true_false', 'True/False')
    )
    
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, null=False)
    created_by = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='questions', null=True)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name='questions')
    tests = models.ManyToManyField(Test, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.text
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(blank=False, null=False)
    isCorrect = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'answers'
    
    def __str__(self):
        return self.text
    
    def is_answer_correct(self):
        # Only check correctness for multiple_choice, single_choice and true_false types
        if self.question.question_type in ['multiple_choice', 'single_choice', 'true_false']:
            return self.isCorrect
        return None
