from rest_framework import serializers

from django.contrib.auth import get_user_model

Usuario = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['dni' ,'password']
        extra_kwargs = {'password': {'write_only' : True}}

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)