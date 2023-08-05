from django.urls import path
from api import views

urlpatterns = [
    path('auth/login/', views.AuthView.as_view()),
    path('customers/', views.CustomerListView.as_view())
]
