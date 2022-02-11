from email import message
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import AcademicianSerializer, ReasonSerializer, PaymentSerializer
from . import models

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


class ReasonsAPIView(APIView):
    def get(self, request):
        reasons = models.Reason.objects.all()
        serializer = ReasonSerializer(reasons, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
