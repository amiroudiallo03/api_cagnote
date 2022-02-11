from django.urls import path
from . import views


urlpatterns = [
    path('academicians', views.api_academiciens),
    path('reasons/', views.ReasonsAPIView.as_view()),
    path('academicians/<str:register_number>', views.api_academician),
]