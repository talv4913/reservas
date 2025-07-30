import datetime

from rest_framework import serializers

from .models import ReservaModel

class ReservaSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['fecha'] < datetime.date.today():
            raise serializers.ValidationError("La fecha no puede ser del pasado")
        return data

    def create(self, validated_data):
        usuario = self.context['request'].user
        if not usuario.is_authenticated:
            raise serializers.ValidationError("Debes estar logueado para hacer una reserva")
        validated_data['usuario'] = usuario
        return super().create(validated_data)

    class Meta:
        model = ReservaModel
        fields = '__all__'
        read_only_fields = ['usuario']

class DisponibilidadSerializer(serializers.Serializer):
    fecha = serializers.DateField()
    comensales = serializers.IntegerField(min_value=1)

    def validate_fecha(self, valor):
        if valor < datetime.date.today():
            raise serializers.ValidationError("La fecha no puede ser del pasado")
        return valor