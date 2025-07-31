from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from .serializers import ReservaSerializer, DisponibilidadSerializer
from .models import ReservaModel
# Create your views here.


class UsuarioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        reservas = ReservaModel.objects.filter(usuario=request.user)
        respuesta = ReservaSerializer(reservas, many=True)
        return Response(respuesta.data,status.HTTP_200_OK)
    
    def post(self,request):
        reserva = ReservaSerializer(data=request.data, context={'request':request})
        if reserva.is_valid():
            reserva.save()
            return Response(reserva.data, status=status.HTTP_201_CREATED)
        return Response(reserva.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk):
        reserva = get_object_or_404(ReservaModel, pk=pk)
        if not reserva.usuario==request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StaffView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        reservas = ReservaModel.objects.all()
        respuesta = ReservaSerializer(reservas, many=True)
        return Response(respuesta.data, status=status.HTTP_200_OK)
    
    def delete(self,request,pk):
        reserva = get_object_or_404(ReservaModel, pk=pk)
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
MAXIMO_COMENSALES = 40

class DisponibilidadView(APIView):
    def get(self,request):
        serializer = DisponibilidadSerializer(data=request.query_params)
        if serializer.is_valid():
            fecha = serializer.validated_data['fecha']
            comensales = serializer.validated_data['comensales']
            respuesta = []
            for bloque in ('18:00','19:00','20:00','21:00','22:00','23:00','00:00'):
                comensales_actuales =0 
                reservas = ReservaModel.objects.filter(fecha=fecha, horario__horario=bloque)
                for reserva in reservas:
                    comensales_actuales += reserva.comensales
                if comensales_actuales + comensales <= MAXIMO_COMENSALES:
                    respuesta.append(bloque)
            return Response(respuesta, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)