from rest_framework import serializers
from .models import AppUser,CertificationList
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'

    def validate(self, attrs):

        password = attrs.get('password')
        if not re.search(r"[a-z]",password): 
            self.errors["lower_case_error"] = "Must contain at least one lowercase letter "
        if not re.search(r"[A-Z]",password):
            self.errors["upper_case_errors"] = "Must contain at least one uppercase letter"
        if not re.search[r"[0-9]",password]:
            self.errors["number_error"] = "Must contain at least one digit"
        if not re.search[r"@$!%*?&#",password]:
            self.errors["special_character"] = "Must contain one special character"
            return self.errors

        return super().validate(attrs)

    def create(self, validated_data):
        user = AppUser.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],  # It hashes internally,
            profile_picture = validated_data['profile_picture']
        )
        return user
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email',instance.email)
        instance.full_name = validated_data.get('full_name',instance.full_name)
        instance.phone_number = validated_data.get('phone_number',instance.phone_number)
        instance.password = validated_data.get('password',instance.password)
        instance.profile_picture = validated_data.get('password',instance.profile_picture)
        return instance
    
class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationList
        fields = '__all__'

    def create(self, validated_data):
        return CertificationList.objects.create(**validated_data)