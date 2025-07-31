import datetime

from rest_framework import serializers

from .models import ReservaModel, BloqueHorario

class ReservaSerializer(serializers.ModelSerializer):
    horario = serializers.PrimaryKeyRelatedField(many=True, queryset=BloqueHorario.objects.all())
    
    def validate(self, data):
        if data['fecha'] < datetime.date.today():
            raise serializers.ValidationError("La fecha no puede ser del pasado")
        return data

    def create(self, validated_data):
        usuario = self.context['request'].user
        if not usuario.is_authenticated:
            raise serializers.ValidationError("Debes estar logueado para hacer una reserva")
        validated_data['usuario'] = usuario
        bloques = validated_data.pop('horario')
        reserva = super().create(validated_data)
        reserva.horario.set(bloques)
        return reserva

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