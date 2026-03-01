from django.urls import path
from .views import LoginView, RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginView.as_view()),

]
