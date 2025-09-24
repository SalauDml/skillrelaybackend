from rest_framework.serializers import ModelSerializer
from .models import Tutor
from rest_framework import serializers

class TutorSerializer (ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'
        read_only_fields = ['user']


    
    # Feature to add: Validation to check if train a teacher module is completed. If not completed add to errors. Filter using user completed model
    def validate(self, attrs):
        errors = {}
        if not attrs["bio"]:
            errors["Bio"] = "Bio is a required field"

        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

    def create(self, validated_data):
        active_user = self.context["request"].user
        active_user.is_staff = True
        active_user.save()
        return Tutor.objects.create(
            user = self.context["request"].user,
            bio = validated_data["bio"]
        )