from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_academiciens),
    path('reasons/', views.ReasonsAPIView.as_view()),
    path('reasons/<int:pk>', views.ReasonAPIView.as_view())
]