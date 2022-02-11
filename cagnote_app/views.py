from email import message
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import AcademicianSerializer, ReasonSerializer, PaymentSerializer
from . import models
import json

# Create your views here.

def academician_exists(register_number: str):
    try:
        academician = models.Academician.objects.get(register_number=register_number)
        return True
    except models.Academician.DoesNotExist: return False, None

@api_view(['GET','POST'])
def api_academiciens(request):

    if request.method == 'GET':
        academician = models.Academician.objects.all()
        serializer = AcademicianSerializer(academician, many=True)
        return Response(serializer.data)

    if request.method == 'POST':

        if academician_exists(request.data.get('register_number')):
            print('verify')
            message = 'Academicien déja enregistré'
            return Response({'message': message,'succes':False})
        else:
            serializer = AcademicianSerializer(data=request.data)
            print('serialize')
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Enregistrement éffectué avec succes', 'sucess':True})
    
    return Response({"message":'bienvenue a oda'})


@api_view(['GET','PUT','DELETE'])
def api_academician(request, register_number):

    try:
        academician = models.Academician.objects.get(register_number=register_number)
    except models.Academician.DoesNotExist:
        message = 'Aucun academiciaen rétrouvé'
        return Response({'message': message, 'succes':False})

    if request.method == 'GET':
        serializer = AcademicianSerializer(academician)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AcademicianSerializer(academician, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = 'Modification éffectuée avec succès.'
            return Response({"message": message, "succes":'succes'})

        return Response({"message":'Aucune modifications éffectué'})

    elif request.method == "DELETE":
        academician.delete()
    message = 'Académicien bien supprimé !'
    success = True
    return Response({"message":message, "success": success})
    





class ReasonsAPIView(APIView):
    def get(self, request):
        reasons = models.Reason.objects.all()
        serializer = ReasonSerializer(reasons, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        message = ''
        success = False
        if not request.data.get('name'):
            message = 'Veuillez remplir le champ requis !'
            return Response({'message': message, success: success}, status=status.HTTP_200_OK)
        # elif len(request.data.keys()) > 1:
        #     message = 'Veuillez envoyer uniquement le nom du motif !'
        #     return Response({'message': message, 'status':status}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if models.Reason.objects.filter(name=request.data.get('name').lower()).exists():
                message = 'Ce motif est déjà enregistré'
                return Response({'message': message, success: success}, status=status.HTTP_200_OK)
            else:
                models.Reason.objects.create(name=request.data.get('name').lower())
                message = 'Motif bien enregistré.'
                success = True
                
                return Response({'message': message, success: success}, status.HTTP_201_CREATED)


class ReasonAPIView(APIView):
    def get(self, request, pk):
        message = ''
        success = False
        if not models.Reason.objects.filter(pk=pk).exists():
            message = "Ce motif n'existe pas !"
            
            return Response({'message': message, 'success':success}, status=status.HTTP_404_NOT_FOUND)
        else:
            reason = models.Reason.objects.get(pk=pk)
            serializer = ReasonSerializer(reason)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk):
        message = ''
        success = False
        if not models.Reason.objects.filter(pk=pk).exists():
            message = "Ce motif n'existe pas !"
            
            return Response({'message': message, 'success':success}, status=status.HTTP_404_NOT_FOUND)
        else:
            if not request.data.get('name'):
                message = "Veuillez remplir le champ requis !"
                
                return Response({'message': message, 'success':success}, status=status.HTTP_200_OK)
            else:
                reason = models.Reason.objects.filter(pk=pk)
                reason.update(name=request.data.get('name'))
                message = 'Motif bien modifié !'
                success = True
                
                return Response({'message': message, 'success':success}, status=status.HTTP_200_OK)
