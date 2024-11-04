from rest_framework import serializers
from questions.models import Question
from .models import Test, Result

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'choices', 'correct_answer']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'questions', 'created_at', 'updated_at']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        test = Test.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(test=test, **question_data)
        return test

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if questions_data:
            for question_data in questions_data:
                question_id = question_data.get('id', None)
                if question_id:
                    # Update existing question
                    question = Question.objects.get(id=question_id, test=instance)
                    question.text = question_data.get('text', question.text)
                    question.choices = question_data.get('choices', question.choices)
                    question.correct_answer = question_data.get('correct_answer', question.correct_answer)
                    question.save()
                else:
                    # Create new question
                    Question.objects.create(test=instance, **question_data)

        return instance

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'test', 'user', 'score', 'submitted_at']

    def create(self, validated_data):
        return Result.objects.create(**validated_data)
