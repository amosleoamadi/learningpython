from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
import traceback
from .serializers import LoginSerializer
from .utils import generate_otp, send_otp_email
from .models import EmailOTP
from .serializers import VerifyEmailSerializer
from .serializers import ResendOTPSerializer
from .serializers import ForgotPasswordSerializer
from .serializers import ResetPasswordSerializer

# Create your views here.
@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={201: RegisterSerializer, 400: "Bad Request"}
)
@api_view(['POST'])
def register(request):
   try:
       serializer = RegisterSerializer(data=request.data)

       if serializer.is_valid():
        user = serializer.save()  # ✅ FIX

        otp = generate_otp()

        EmailOTP.objects.create(user=user, code=otp)

        send_otp_email(user.email, otp)

        return Response({
            "success": True,
            "message": "User registered successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
            
       return Response({
                "success": False,
                "error": serializer.errors,
            }, status=400)
   
   except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
   
   

@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        user = data['user']

        return Response({
            "success": True,
            "message": "Login successful",
            "data": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "access_token": data['access'],
                "refresh_token": data['refresh']
            }
        })

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)



@swagger_auto_schema(
    method='post',
    request_body=VerifyEmailSerializer,
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
def verify_email(request):
    serializer = VerifyEmailSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        otp_obj = serializer.validated_data['otp_obj']

        # ✅ Mark user as verified
        profile = user.profile
        profile.is_verified = True
        profile.save()

        # 🧹 Delete OTP after use
        otp_obj.delete()

        return Response({
            "success": True,
            "message": "Email verified successfully"
        })

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=ResendOTPSerializer,
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
def resend_otp(request):
    serializer = ResendOTPSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        # 🔍 Check last OTP BEFORE deleting
        last_otp = EmailOTP.objects.filter(user=user).order_by('-created_at').first()

        if last_otp and last_otp.is_valid():
            return Response({
                "success": False,
                "error": "Wait before requesting another OTP"
            }, status=400)

        # 🧹 Now delete old OTPs
        EmailOTP.objects.filter(user=user).delete()

        # 🔢 Generate new OTP
        otp = generate_otp()

        # 💾 Save new OTP
        EmailOTP.objects.create(user=user, code=otp)

        # 📧 Send email
        send_otp_email(user.email, otp)

        return Response({
            "success": True,
            "message": "OTP resent successfully"
        })

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)


@swagger_auto_schema(
    method='post',
    request_body=ForgotPasswordSerializer,
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        # 🧹 Delete old OTPs
        EmailOTP.objects.filter(user=user).delete()

        # 🔢 Generate OTP
        otp = generate_otp()

        # 💾 Save OTP
        EmailOTP.objects.create(user=user, code=otp)

        # 📧 Send email
        send_otp_email(user.email, otp)

        return Response({
            "success": True,
            "message": "OTP sent to email"
        })

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)


@swagger_auto_schema(
    method='post',
    request_body=ResetPasswordSerializer,
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        otp_obj = serializer.validated_data['otp_obj']
        new_password = serializer.validated_data['new_password']

        # 🔐 Set new password
        user.set_password(new_password)
        user.save()

        # 🧹 Delete OTP
        otp_obj.delete()

        return Response({
            "success": True,
            "message": "Password reset successful"
        })

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)