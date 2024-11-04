from django.urls import path
from .views import ListCreateQuestionView, UpdateDeleteQuestionView

urlpatterns = [
    path('', ListCreateQuestionView.as_view()),
    path('<int:pk>', UpdateDeleteQuestionView.as_view()),
]