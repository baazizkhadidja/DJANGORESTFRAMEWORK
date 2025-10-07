from rest_framework import serializers
from .models import Product, Category
from django.contrib.auth.models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data.get('email'),
#             password=validated_data['password']
#         )
#         return user





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # Display category name when reading data
    categorie_name = serializers.StringRelatedField(source='categorie', read_only=True)
    # Use ID (or dropdown) when creating/updating
    categorie = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    
    class Meta:
        model = Product
        fields = ['id','title', 'price', 'categorie', 'categorie_name']