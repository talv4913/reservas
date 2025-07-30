from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import ReservaSerializer, DisponibilidadSerializer
from .models import Usuario, ReservaModel
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