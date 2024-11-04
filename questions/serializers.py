from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'isCorrect']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'created_by', 'category', 'answers']

    def validate(self, data):
        question_type = data.get('question_type')
        answers = data.get('answers', [])

        if question_type == 'multiple_choice':
            if len(answers) < 2:
                raise serializers.ValidationError("Multiple Choice questions must have at least 2 answers.")
            if not any(answer['isCorrect'] for answer in answers):
                raise serializers.ValidationError("At least one answer must be marked as correct.")

        elif question_type == 'single_choice':
            if len(answers) < 1:
                raise serializers.ValidationError("Single Choice questions must have at least one answer.")
            if sum(answer['isCorrect'] for answer in answers) != 1:
                raise serializers.ValidationError("Only one answer can be marked as correct.")

        elif question_type == 'true_false':
            if len(answers) != 2:
                raise serializers.ValidationError("True/False questions must have exactly 2 answers: True and False.")
            if sum(answer['isCorrect'] for answer in answers) != 1:
                raise serializers.ValidationError("One answer must be marked as correct (True or False).")

        return data

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', None)
        instance.text = validated_data.get('text', instance.text)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.category = validated_data.get('category', instance.category)
        instance.save()

        if answers_data is not None:
            for answer_data in answers_data:
                answer_id = answer_data.get('id')
                if answer_id:
                    answer = get_object_or_404(Answer, id=answer_id, question=instance)
                    answer.text = answer_data.get('text', answer.text)
                    answer.isCorrect = answer_data.get('isCorrect', answer.isCorrect)
                    answer.save()
                else:
                    Answer.objects.create(question=instance, **answer_data)

        return instance
