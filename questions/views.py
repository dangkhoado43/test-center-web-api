from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Question
from .serializers import QuestionSerializer

class ListCreateQuestionView(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=self.request.user)

            return Response({
                'message': 'Create a new question successful!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message': 'Create a new question unsuccessful!',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateDeleteQuestionView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.get_serializer(question, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'message': 'Update Question successful!',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Update Question unsuccessful!',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        question.delete()

        return Response({
            'message': 'Delete Question successful!'
        }, status=status.HTTP_200_OK)
