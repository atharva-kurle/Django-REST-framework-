from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('index/book-all/', views.fetchAllRecords, name="fetchAllRecords"),
    path('index/book-update/<str:id>/', views.updateBook, name="updateBook"),
    path('index/book-delete/<str:id>/', views.deleteBook, name="deleteBook"),
    path('index/book-create/', views.createBook, name="createBook"),
    path('index/', views.index, name="index"),
    path('student-view/', views.student_view, name="student_view"),
    path('logout/', views.logout, name="logout"),
]