from django.urls import path
from . import views

urlpatterns = [
    # public api
    path('books/', views.BookList.as_view()),
    
    # authenticated users only
    path('user/books/', views.UserBookList.as_view()),
    path('user/create/', views.UserBookCreate.as_view()),
    # to edit only the description
    path('user/edit/<int:pk>', views.UserBookEdit.as_view()),
    path('user/edit/<int:pk>/complete', views.UserBookCompleted.as_view()),

    # Authorization
    path('user/signup/', views.signup),
    path('user/login/', views.login),
]