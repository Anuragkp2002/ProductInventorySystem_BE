from rest_framework import serializers
from .models import Products, ProductsVariation, Attributes, AttributeValues, VariationAttributes
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        print("validated_data: ", validated_data)
        # Create user with hashed password
        user = User.objects.create_user(**validated_data)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        read_only_fields = ['email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    # def validate(self, data):
    #     user = authenticate(email=data['email'], password=data['password'])
    #     if not user:
    #         raise serializers.ValidationError("Invalid login credentials")
    #     return user


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValues
        fields = ('id', 'AttributeValue')


class VariationAttributesSerializer(serializers.ModelSerializer):
    AttributeValue = AttributeValueSerializer()

    class Meta:
        model = VariationAttributes
        fields = ('id', 'AttributeValue')


class ProductsVariationSerializer(serializers.ModelSerializer):
    attributes = VariationAttributesSerializer(many=True)

    class Meta:
        model = ProductsVariation
        fields = ('id', 'DisplayName', 'ProductCode',
                  'ProductImage', 'TotalStock', 'attributes')


class ProductsSerializer(serializers.ModelSerializer):
    variations = ProductsVariationSerializer(many=True)

    class Meta:
        model = Products
        # fields = ('id', 'ProductID', 'ProductCode', 'ProductName', 'ProductImage', 'CreatedDate', 'UpdatedDate', 'CreatedUser', 'IsFavourite', 'Active', 'HSNCode', 'TotalStock', 'variations')
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ('id', 'AttributeName')


class AttributeValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValues
        fields = ('id', 'Attribute', 'AttributeValue')
