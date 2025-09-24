from rest_framework import serializers
from .models import Course, Module, Lesson, Quiz, Questions, Options, Exam, ExamQuestion, ExamChoice,UserCourseProgress


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
    quiz = QuizSerializer(read_only = True)

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

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseProgress
        fields = ['id','course','current_module','current_lesson']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        object = UserCourseProgress.objects.create(
            user = self.context.get("user"), 
            course = validated_data['course'], 
            current_module = validated_data['current_module'], 
            current_lesson = validated_data['current_lesson']  )
        return object
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)