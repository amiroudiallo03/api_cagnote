from django.urls import path
from . import views

app_name = 'cagnote_app'

urlpatterns = [
    path("academicians/", views.api_academiciens, name='index'),
    path("reasons/", views.ReasonsAPIView.as_view(), name='reasons'),
    path("reasons/<int:pk>", views.ReasonAPIView.as_view(), name='reason'),
    # path("academicians", views.api_academiciens),
    path(
        "academicians/<str:register_number>", 
        views.api_academician,
        name='academician'
        ),
    path("payment/", views.api_payment, name='payment'),
    path(
        "payment/paymentbydate/", 
        views.payment_by_date, 
        name='payment_by_date'
        ),
    path("payment/api_caisse/", views.api_caisse, name='money_box'),
    path('academicians/payment/ranking/<int:numbers>/', views.ranking, name='ranking'),
]
 