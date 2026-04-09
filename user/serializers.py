from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EmailOTP

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')

        username = (first_name + last_name).replace(" ", "").lower()

        if User.objects.filter(username=username).exists():
            username += "123"

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(email=email).first()

        if not user.profile.is_verified:
            raise serializers.ValidationError("Email not verified")

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        # 🔥 Generate tokens
        refresh = RefreshToken.for_user(user)

        data['user'] = user
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)

        return data
    

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found")

        otp_obj = EmailOTP.objects.filter(user=user, code=otp).first()

        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP or OTP expired")

        if not otp_obj.is_valid():
            raise serializers.ValidationError("Invalid OTP or OTP expired")

        data['user'] = user
        data['otp_obj'] = otp_obj

        return data
    

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found")

        if user.profile.is_verified:
            raise serializers.ValidationError("User already verified")

        data['user'] = user
        return data
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found")

        data['user'] = user
        return data
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found")

        otp_obj = EmailOTP.objects.filter(user=user, code=otp).first()

        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP")

        if not otp_obj.is_valid():
            raise serializers.ValidationError("OTP expired")

        data['user'] = user
        data['otp_obj'] = otp_obj

        return data