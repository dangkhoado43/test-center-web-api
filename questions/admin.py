from django import forms
from django.contrib import admin
from .models import (QuestionCategory, Question, Answer)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = '__all__'

#     def clean(self):
#         cleaned_data = super().clean()
#         question_type = cleaned_data.get("question_type")
#         answers = self.data.getlist('answer_set-0-text')  # Adjust according to your inline form structure

#         if question_type == 'multiple_choice' and len(answers) < 2:
#             raise forms.ValidationError("Multiple Choice questions must have at least 2 answers.")

#         if question_type == 'single_choice' and answers.count('') > 0:
#             raise forms.ValidationError("Single Choice questions must have at least one answer.")

#         if question_type == 'true_false' and len(answers) != 2:
#             raise forms.ValidationError("True/False questions must have exactly 2 answers: True and False.")

#         return cleaned_data

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = '__all__'

#     def clean(self):
#         cleaned_data = super().clean()
#         question_type = cleaned_data.get("question_type")
        
#         # Fetch all answers
#         answers = self.data.getlist('answer_set-0-text')  # Adjust this if your naming scheme is different
#         correct_answers = self.data.getlist('answer_set-0-isCorrect')  # Fetch correct answer indicators

#         # Validate based on question type
#         if question_type == 'multiple_choice':
#             if len(answers) < 2:
#                 raise forms.ValidationError("Multiple Choice questions must have at least 2 answers.")
#             if not any(correct_answers):  # Ensure at least one answer is marked as correct
#                 raise forms.ValidationError("At least one answer must be marked as correct.")

#         elif question_type == 'single_choice':
#             if len(answers) < 1:
#                 raise forms.ValidationError("Single Choice questions must have at least one answer.")
#             if correct_answers.count('on') != 1:  # Only one correct answer allowed
#                 raise forms.ValidationError("Only one answer can be marked as correct.")

#         elif question_type == 'true_false':
#             if len(answers) != 2:
#                 raise forms.ValidationError("True/False questions must have exactly 2 answers: True and False.")
#             if correct_answers.count('on') != 1:  # One must be correct
#                 raise forms.ValidationError("One answer must be marked as correct (True or False).")

#         return cleaned_data

@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_by', 'created_at', 'updated_at', 'question_type', 'category')
    list_filter = ('created_by', 'question_type', 'category')
    inlines = [AnswerInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Exclude the created_by field from the form
        form.base_fields.pop('created_by', None)
        return form
