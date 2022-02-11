from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_academiciens),
    path('reasons/', views.ReasonsAPIView.as_view()),
    path('reasons/<int:pk>', views.ReasonAPIView.as_view()),
    path('academicians', views.api_academiciens),
    path('reasons/', views.ReasonsAPIView.as_view()),
    path('academicians/<str:register_number>', views.api_academician),
    path('payment', views.api_payment),
    path('payment/paymentbydate', views.payment_by_date),
]