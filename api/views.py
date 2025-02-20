from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.generics import CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny

from api.filters import BookFilter
from api.mixins import SuperGenericAPIViews, UltraModelViewSet
from api.paginations import SimplePagination
from api.permissions import IsAdminOrReadOnly, IsAuthor, IsOwner, IsOwnerOrReadOnly
from api.serializers import BookImageSerializer, CategorySerializer, CreateBookSerializer, DetailBookSerializer, GenreSerializer, ListBookSerializer, RegisterSerializer,TagSerializer, UpdateBookSerializer
from book.models import Book, BookImage, Category, Genre, Tag
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class RegisterView(generics.CreateAPIView):

    queryset = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "Пользователь создан"}, 
            status=status.HTTP_201_CREATED
        )


class BookViewSet(UltraModelViewSet):
    queryset = Book.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': ListBookSerializer,
        'retrieve': DetailBookSerializer,
        'create': CreateBookSerializer,
        'update': UpdateBookSerializer,
    }

    pagination_class = SimplePagination
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    search_field = ['name', 'description', 'content', 'author_book']    
    ordering_fields = ['name', 'is_published', 'rating', 'views']


    permission_classes_by_action = {
        'list':  [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated, IsAuthor],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }
    

class ImageViewSet(UltraModelViewSet):
    queryset = BookImage.objects.all()
    lookup_field = 'id'
    serializer_class = BookImageSerializer

    permission_classes_by_action = {
        'list':  [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated, IsAuthor],
        'update': [IsAuthenticated],
        'destroy': [IsAuthenticated,],
    }


# class CreateImageApiView(SuperGenericAPIViews):
#     serializer_class = BookImageSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

# class DeleteImageApiView(SuperGenericAPIViews):
#     queryset = BookImage.objects.all()
#     lookup_field = 'id'


#     def delete(self, request, *args, **kwargs):
#         book_image = self.get_object()
#         book_image.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class TagViewSet(UltraModelViewSet):
    queryset = Tag.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
    # filter_backends = [
    #     SearchFilter,
    #     DjangoFilterBackend,
    #     OrderingFilter,
    # ]

    permission_classes_by_action = {
        'list':  [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated,],
        'update': [IsAuthenticated, ],
        'destroy': [IsAuthenticated,]
    }


class GenreViewSet(UltraModelViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'id'
    serializer_class = GenreSerializer

    # permission_classes_by_action = {
    #     'list':  [AllowAny],
    #     'retrieve': [AllowAny],
    #     'create': [IsAuthenticated, IsAuthor],
    #     'update': [IsAuthenticated],
    #     'destroy': [IsAuthenticated],
    # }

class CategoryViewSet(UltraModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': CategorySerializer,
        'retrieve': CategorySerializer,
        'create': CategorySerializer,
        'update': CategorySerializer,
    }
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    permission_classes_by_action = {
        'list':  [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated, IsAuthor],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }


# class ListCreateTagApiView(SuperGenericAPIViews):

#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

#     def get(self, request, *args, **kwargs):
#         tags = self.get_queryset()
#         serializer = self.get_serializer(tags,many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         tags = serializer.save()
#         read_serializer = self.get_response_serializer(tags)
#         return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
# class UpdateDeleteBookTagApiView(SuperGenericAPIViews):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer

#     permission_classes = [IsAuthenticatedOrReadOnly,]

#     lookup_field = 'id'
#     # lookup_url_kwarg = 'id'

#     def update(self, request, partial):
#         tag = self.get_object()
#         serializer = self.get_serializer(instance=tag, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         tag = serializer.save()
#         read_serializer = self.get_serializer(tag)
#         return Response(read_serializer.data)

#     def get(self, request, *args, **kwargs):
#         tag = self.get_object()
#         serializer = self.get_serializer(tag)
#         return Response(serializer.data)

#     def patch(self, request, *args, **kwargs):
#         return self.update(request, True)

#     def put(self, request, *args, **kwargs):
#         return self.update(request,  False)

#     def delete(self, request,*args, **kwargs):
#         tag = self.get_object()
#         tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
   

# class ListCreateGenreApiView(SuperGenericAPIViews):

#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     response_serializer = GenreSerializer 
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request, *args, **kwargs):
#         genres = self.get_queryset()
#         serializer = self.get_serializer(genres,many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         genres = serializer.save()
#         read_serializer = self.get_response_serializer(genres)
#         return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
# class UpdateDeleteBookGenreApiView(SuperGenericAPIViews):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def update(self, request, partial):
        genre = self.get_object()
        serializer = self.get_serializer(instance=genre, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        genre = serializer.save()
        read_serializer = self.get_serializer(genre)
        return Response(read_serializer.data)

    def get(self, request, *args, **kwargs):
        genre = self.get_object()
        serializer = self.get_serializer(genre)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.update(request,  True)

    def put(self, request, *args, **kwargs):
        return self.update(request,  False)

    def delete(self, request,*args, **kwargs):
        genre = self.get_object()
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class ListCreateCategoryApiView(SuperGenericAPIViews):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

#     def get(self, request, *args, **kwargs):
#         categories = self.get_queryset()
#         serializer = self.get_serializer(categories,many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         categories = serializer.save()
#         read_serializer = self.get_response_serializer(categories)
#         return Response(read_serializer.data, status=status.HTTP_201_CREATED)    

# class UpdateDeleteBookCategory(GenericAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     lookup_field = 'id'
#     lookup_url_kwarg = 'id'

#     def update(self, request, partial):
#         category = self.get_object()
#         serializer = self.get_serializer(instance=category, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         category = serializer.save()
#         read_serializer = self.get_serializer(category)
#         return Response(read_serializer.data)

#     def get(self, request, *args, **kwargs):
#         category = self.get_object()
#         serializer = self.get_serializer(category)
#         return Response(serializer.data)

#     def patch(self, request, *args, **kwargs):
#         return self.update(request,  True)

#     def put(self, request, *args, **kwargs):
#         return self.update(request,  False)

#     def delete(self, request,*args, **kwargs):
#         category = self.get_object()
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
