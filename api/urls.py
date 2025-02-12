from django.urls import include, path
from . import views

urlpatterns = [
    path('books/', views.ListCreateBookApiView.as_view()),
    path('books/<int:id>/', views.UpdateDeleteDetailBookApiView.as_view()),

    path('book-images/', views.CreateImageApiView.as_view()),
    path('book-images/<int:id>/', views.DeleteImageApiView.as_view()),


    path('categories/', views.ListCreateCategoryApiView.as_view()),
    path('categories/<int:id>/', views.UpdateDeleteBookCategory.as_view()),
    
    path('tags/', views.ListCreateTagApiView.as_view()),
    path('tags/<int:id>/', views.UpdateDeleteBookTagApiView.as_view()),

    path('genres/', views.ListCreateGenreApiView.as_view()),
    path('genres/<int:id>/', views.UpdateDeleteBookGenreApiView.as_view()),

    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('auth/', include('api.auth.urls')),
]



