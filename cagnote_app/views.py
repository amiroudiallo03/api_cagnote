from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    AcademicianSerializer,
    ReasonSerializer,
    PaymentSerializer,
    CaisseSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import models
from datetime import date
from django.db.models import Q
import json


# Create your views here.


def academician_exists(register_number: str):
    try:
        academician = models.Academician.objects.get(register_number=register_number)
        return True
    except models.Academician.DoesNotExist:
        return False

@swagger_auto_schema(methods=['GET'], responses={200: openapi.Response('Renvoie tous les académiciens', AcademicianSerializer)})
@swagger_auto_schema(methods=['POST'], request_body=AcademicianSerializer, responses={201: openapi.Response('Crée un nouveau académicien')})
@api_view(["GET", "POST"])
def api_academiciens(request):

    if request.method == "GET":
        academician = models.Academician.objects.all()
        serializer = AcademicianSerializer(academician, many=True)
        return Response(serializer.data)

    if request.method == "POST":

        if academician_exists(request.data.get("register_number")):
            message = "Academicien déja enregistré"
            return Response({"message": message, "succes": False})
        else:
            serializer = AcademicianSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Enregistrement éffectué avec succes", "sucess": True}
                )

    return Response({"message": "bienvenue a oda"})


@swagger_auto_schema(methods=['PUT'], request_body=AcademicianSerializer, responses={200: openapi.Response('Modifie un académicien selon son matricule')})
@swagger_auto_schema(methods=['GET'], responses={200: openapi.Response('Affiche un académicien selon son matricule', AcademicianSerializer)})
@swagger_auto_schema(methods=['DELETE'], responses={204: openapi.Response('supprime un académicien selon son matricule')})
@api_view(["GET", "PUT", "DELETE"])
def api_academician(request, register_number):

    try:
        academician = models.Academician.objects.get(register_number=register_number)
    except models.Academician.DoesNotExist:
        message = "Aucun academicien rétrouvé"
        return Response({"message": message, "succes": False})

    if request.method == "GET":
        serializer = AcademicianSerializer(academician)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = AcademicianSerializer(academician, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Modification éffectuée avec succès."
            return Response({"message": message, "succes": "succes"})

        return Response({"message": "Aucune modifications éffectué"})

    elif request.method == "DELETE":
        academician.delete()
    message = "Académicien bien supprimé !"
    success = True
    return Response({"message": message, "success": success})


@api_view(["GET", "POST"])
def api_payment(request):
    message = ""
    success = False
    if request.method == "GET":
        payment = models.Payment.objects.all()
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        matricule = request.data.get("register_number")
        try:
            academicien = models.Academician.objects.get(register_number=matricule)
        except:
            messages = "Erreur: Académicien introuvable !"
            return Response({"message": messages, "success": success})
        else:

            # academicien = models.Academician.objects.get(register_number=matricule)
            motif_id = request.data.get("reason")
            reason = models.Reason.objects.filter(name=motif_id)
            if not models.Reason.objects.filter(name=motif_id).exists():
                message = "Motif inexistant"
                return Response({"message": message, "success": success})
            # if models.Payment.objects.filter(academician=academicien).exists():
            #    message = "Payment déjà éffectué pour ce motif aujourd'hui "
            #    return Response({"message":message, "success": success})
            else:
                try:
                    motif = models.Reason.objects.get(name=motif_id)
                    pay = models.Payment.objects.create(
                        academician=academicien,
                        reason=motif,
                        montant=request.data.get("montant"),
                    )
                    pay.save()
                    message = "Payment effectué avec success"
                    success = True
                    return Response({"message": message, "success": success})
                except:
                    message = "Payment déjà éffectué pour ce motif"
                    success = False
                    return Response({"message": message, "success": success})


@api_view(["GET"])
def payment_by_date(request):

    if request.method == "GET":
        date_payment = request.data.get("date_payment")
        reason = request.data.get("reason")
        payment = models.Payment.objects.filter(
            Q(payment_date=date_payment) | Q(reason=reason)
        )
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)


import re


@api_view(["GET"])
def api_caisse(request):
    if request.method == "GET":
        payment = models.Payment.objects.values_list("montant", flat=True)
        caisse = str(payment)
        montant = re.findall("\d+", caisse)
        box = [int(i) for i in montant]
        montant_caisse = sum(box)
        return Response({"montant_caisse": f"{montant_caisse}"})

    return Response({'message':'Solde'})

class ReasonsAPIView(APIView):
    def get(self, request):
        reasons = models.Reason.objects.all()
        serializer = ReasonSerializer(reasons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        message = ""
        success = False
        if not request.data.get("name"):
            message = "Veuillez remplir le champ requis !"
            return Response(
                {"message": message, success: success}, status=status.HTTP_200_OK
            )
        # elif len(request.data.keys()) > 1:
        #     message = 'Veuillez envoyer uniquement le nom du motif !'
        #     return Response({'message': message, 'status':status}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if models.Reason.objects.filter(
                name=request.data.get("name").lower()
            ).exists():
                message = "Ce motif est déjà enregistré"
                return Response(
                    {"message": message, success: success}, status=status.HTTP_200_OK
                )
            else:
                models.Reason.objects.create(name=request.data.get("name").lower())
                message = "Motif bien enregistré."
                success = True

                return Response(
                    {"message": message, success: success}, status.HTTP_201_CREATED
                )


class ReasonAPIView(APIView):
    def get(self, request, pk):
        message = ""
        success = False
        if not models.Reason.objects.filter(pk=pk).exists():
            message = "Ce motif n'existe pas !"

            return Response(
                {"message": message, "success": success},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            reason = models.Reason.objects.get(pk=pk)
            serializer = ReasonSerializer(reason)

            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        message = ""
        success = False
        if not models.Reason.objects.filter(pk=pk).exists():
            message = "Ce motif n'existe pas !"

            return Response(
                {"message": message, "success": success},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            if not request.data.get("name"):
                message = "Veuillez remplir le champ requis !"

                return Response(
                    {"message": message, "success": success}, status=status.HTTP_200_OK
                )
            else:
                reason = models.Reason.objects.filter(pk=pk)
                reason.update(name=request.data.get("name"))
                message = "Motif bien modifié !"
                success = True

                return Response(
                    {"message": message, "success": success}, status=status.HTTP_200_OK
                )

    def delete(self, request, pk):
        message = ""
        success = False
        if not models.Reason.objects.filter(pk=pk).exists():
            message = "Ce motif n'existe pas !"

            return Response(
                {"message": message, "success": success},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            reason = models.Reason.objects.filter(pk=pk)
            reason.delete()
            message = "Motif bien supprimé."
            success = True

            return Response(
                {"message": message, "success": success}, status=status.HTTP_200_OK
            )

def home(request):
    return redirect('cagnote_app:index')

@api_view(['GET'])
def ranking(request, numbers):
    academicians = models.Academician.objects.all()[:numbers]
    serializer = AcademicianSerializer(academicians, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)