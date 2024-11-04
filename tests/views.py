from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from questions.models import Question
from .models import Test, Result
from .serializers import TestSerializer, QuestionSerializer, ResultSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Retrieve a list of all tests."""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new test."""
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        """Retrieve detailed information about a test by ID."""
        return super().retrieve(request, pk=pk)

    def update(self, request, pk=None):
        """Update test information by ID."""
        return super().update(request, pk=pk)

    def destroy(self, request, pk=None):
        """Delete a test by ID."""
        return super().destroy(request, pk=pk)


class TestTakeView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, test_id):
        """Start taking a test."""
        try:
            test = Test.objects.get(id=test_id)
            questions = test.questions.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response({"detail": "Test not found."}, status=status.HTTP_404_NOT_FOUND)


class TestResultSubmitView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, test_id):
        """Submit test results."""
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(test_id=test_id, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
