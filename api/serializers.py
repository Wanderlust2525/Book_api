import uuid
from book.models import *
from rest_framework import serializers

from utils.main import base64_to_image_file

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class ImageForBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookImage
        exclude = ('books',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)



class ListBookSerializer(serializers.ModelSerializer):

    # user = UserSerializer()
    image = serializers.ImageField()
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    genres = GenreSerializer(many=True)
    images = ImageForBookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        exclude = ('content',)


class DetailBookSerializer(serializers.ModelSerializer):
    

    image = serializers.ImageField()
    category = CategorySerializer()
    tags = TagSerializer(many = True)
    genres = GenreSerializer(many=True)
    images = ImageForBookSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class CreateTagSerializer(serializers.Serializer):

    class Meta:
        model = Tag
        exclude = ('book', 'user',)

class CreateBookSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.CharField(),required = False)
    class Meta:
        model = Book
        fields = '__all__'
        
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        tags = validated_data.pop('tags', [])
        genres = validated_data.pop('genres', [])
        file_images = []
        for image in images:
            try:
                file = base64_to_image_file(image, uuid.uuid4())
                file_images.append(file)
            except Exception as e:
                print(e)
                raise serializers.ValidationError(
                    {'images': ['Загрузите корректное изображение']}
                )
        book = Book.objects.create(**validated_data)
        book.tags.add(*tags)
        book.genres.add(*genres)
        
        for file_image in file_images:
            book_image = BookImage.objects.create(book=book)
            book_image.image.save(file_image.name, file_image)
            book_image.save()
        return book
    

class UpdateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('user',)

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'email', 'first_name', 'last_name',]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
