from rest_framework import serializers
from .models import AppUser,CertificationList
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'

    def validate(self, attrs):

        errors = {}

        password = attrs.get('password')
        if not re.search(r"[a-z]",password): 
            errors["lower_case_error"] = "Must contain at least one lowercase letter "
        if not re.search(r"[A-Z]",password):
            errors["upper_case_errors"] = "Must contain at least one uppercase letter"
        if not re.search(r"[0-9]",password):
            errors["number_error"] = "Must contain at least one digit"
        if not re.search(r"[@$!%*?&#]",password):
            errors["special_character"] = "Must contain one special character"
        if errors:
            raise serializers.ValidationError(errors)

        return attrs

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
        instance.first_name = validated_data.get('full_name',instance.first_name)
        instance.last_name = validated_data.get('full_name',instance.last_name)
        instance.middle_name = validated_data.get('full_name',instance.middle_name)
        instance.phone = validated_data.get('phone_number',instance.phone)
        instance.password = validated_data.get('password',instance.password)
        instance.profile_picture = validated_data.get('password',instance.profile_picture)
        return instance
    
class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationList
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        return CertificationList.objects.create(
            user = self.context["request"].user,
            file = validated_data["file"]
        )
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access_token = refresh.access_token

        # Add extra token meta info
        data['expires_at'] = datetime.fromtimestamp(access_token['exp'])
        data['issued_at'] = datetime.fromtimestamp(access_token['iat'])
        data['lifetime_seconds'] = access_token['exp'] - access_token['iat']
        data['token_type'] = access_token['token_type']

        return data 
