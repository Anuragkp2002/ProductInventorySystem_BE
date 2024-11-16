from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Products, ProductsVariation, Attributes, AttributeValues, VariationAttributes, Variant, Option
from .serializers import ProductsSerializer, ProductsVariationSerializer, UserSignupSerializer, UserProfileSerializer, UserUpdateProfileSerializer, LoginSerializer, TokenSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Prefetch


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
            # Authenticate user
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

    @swagger_auto_schema(
        operation_description="Update user profile",
        responses={200: UserProfileSerializer()},
    )
    def put(self, request):
        serializer = UserUpdateProfileSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete user account",
        responses={204: 'Account deleted successfully'},
    )
    def delete(self, request):
        user = request.user
        user.delete()
        print("Deleted User: ",user)
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            product_data = request.data

            try:
                created_user_id = product_data.get("CreatedUser")
                product = Products.objects.create(
                    ProductID=product_data.get("ProductID"),
                    ProductCode=product_data.get("ProductCode"),
                    ProductName=product_data.get("ProductName"),
                    ProductImage=product_data.get("ProductImage", None),
                    CreatedUser_id=created_user_id,
                    IsFavourite=product_data.get("IsFavourite", False),
                    Active=product_data.get("Active", True),
                    HSNCode=product_data.get("HSNCode", None),
                    TotalStock=product_data.get("TotalStock", 0.00)
                )

                for variant_data in product_data.get("variants", []):
                    variation = ProductsVariation.objects.create(
                        Product=product,
                        DisplayName=variant_data["name"],
                        ProductCode=variant_data["name"].upper(),
                        TotalStock=product_data.get("TotalStock", 0.00)
                    )

                    for option_name in variant_data.get("options", []):
                        variant = Variant.objects.create(
                            product=variation,
                            name=option_name
                        )
                        Option.objects.create(
                            variant=variant,
                            name=option_name
                        )

                serializer = ProductsSerializer(product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        
        serializer = ProductsSerializer(products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post_add_stock(self, request, *args, **kwargs):
        product_variation_id = request.data.get("variation_id")
        stock_quantity = request.data.get("stock_quantity", 0)
        product = request.data.get("product")
        
        if not product_variation_id or stock_quantity <= 0:
            return Response({"error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_variation = ProductsVariation.objects.get(id=product_variation_id, Product=product)

            product_variation.TotalStock += stock_quantity
            product_variation.save()

            return Response({"status": "Stock added successfully."}, status=status.HTTP_200_OK)

        except ProductsVariation.DoesNotExist:
            return Response({"error": "Product variation not found."}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def post_remove_stock(self, request, *args, **kwargs):
        product_variation_id = request.data.get("variation_id")
        stock_quantity = request.data.get("stock_quantity", 0)
        
        if not product_variation_id or stock_quantity <= 0:
            return Response({"error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_variation = ProductsVariation.objects.get(id=product_variation_id)

            if product_variation.TotalStock < stock_quantity:
                return Response({"error": "Insufficient stock to remove."}, status=status.HTTP_400_BAD_REQUEST)

            product_variation.TotalStock -= stock_quantity
            product_variation.save()

            return Response({"status": "Stock removed successfully."}, status=status.HTTP_200_OK)

        except ProductsVariation.DoesNotExist:
            return Response({"error": "Product variation not found."}, status=status.HTTP_404_NOT_FOUND)
  


# class AttributeViewSet(viewsets.ModelViewSet):
#     queryset = Attributes.objects.all()
#     serializer_class = AttributeSerializer
#     permission_classes = [IsAuthenticated]


# class AttributeValueViewSet(viewsets.ModelViewSet):
#     queryset = AttributeValues.objects.all()
#     serializer_class = AttributeValueCreateSerializer
#     permission_classes = [IsAuthenticated]
