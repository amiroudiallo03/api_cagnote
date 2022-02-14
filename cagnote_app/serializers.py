from dataclasses import field
from cagnote_app.models import Academician, Reason, Payment
from rest_framework import serializers


class AcademicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academician
        exclude = ["date_add", "date_update", "status", "overall_payment"]
        depth = 1


# serializer from Reasons


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        exclude = ["date_add", "date_update", "status"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ["date_add", "date_update", "status"]
        depth = 2


class PaymentRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "academician",
        ]


class CaisseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "montant",
        ]
