from rest_framework import serializers
from .models import Course, Module, Lesson, Quiz, Questions, Options, Exam, ExamQuestion, ExamChoice


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    quiz = QuizSerializer(many = True, read_only = True)

    class Meta:
        model = Module
        fields = '__all__'

class ExamChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamChoice
        fields = '__all__'

class ExamQuestionSerializer(serializers.ModelSerializer):
    choices = ExamChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = ExamQuestion
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    questions = ExamQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    exam = ExamSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'