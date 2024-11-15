from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Products, ProductsVariation, Attributes, AttributeValues
from .serializers import UserSignupSerializer, UserProfileSerializer, UserSignupSerializer, LoginSerializer, TokenSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema


# class ObtainJWTToken(APIView):
#     def post(self, request, *args, **kwargs):
#         user = authenticate(username=request.data.get(
#             'username'), password=request.data.get('password'))
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#             })
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSignupSerializer,
        responses={201: 'User created successfully', 400: 'Bad request'},
    )
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login and get JWT tokens",
        request_body=LoginSerializer,
        responses={200: 'Login successful with tokens',
                   400: 'Invalid credentials'},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            user = authenticate(
                username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={200: UserProfileSerializer()},
    )
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
