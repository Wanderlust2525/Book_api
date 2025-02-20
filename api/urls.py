from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as url_doc

router = DefaultRouter()
router.register('books', views.BookViewSet)
router.register('images', views.ImageViewSet)
router.register('categories', views.CategoryViewSet,basename='category')
router.register('tags', views.TagViewSet)
router.register('genres', views.GenreViewSet)


urlpatterns = [

    # path('book-images/', views.CreateImageApiView.as_view()),
    # path('book-images/<int:id>/', views.DeleteImageApiView.as_view()),


    # path('categories/', views.ListCreateCategoryApiView.as_view()),
    # path('categories/<int:id>/', views.UpdateDeleteBookCategory.as_view()),
    
    # path('tags/', views.ListCreateTagApiView.as_view()),
    # path('tags/<int:id>/', views.UpdateDeleteBookTagApiView.as_view()),

    # path('genres/', views.ListCreateGenreApiView.as_view()),
    # path('genres/<int:id>/', views.UpdateDeleteBookGenreApiView.as_view()),

    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls))
]

urlpatterns += url_doc

