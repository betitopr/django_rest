from rest_framework import serializers
from django.contrib.auth import get_user_model  
from .models import InternetPlan, ClientService
from apps.accounts.serializers import UserSerializer

# Obtener el modelo User configurado en settings
User = get_user_model()

class InternetPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternetPlan
        fields = '__all__'

class ClientServiceSerializer(serializers.ModelSerializer):
     # Incluye los datos completos del usuario usando UserSerializer
    client = UserSerializer(read_only=True)
     # Incluye los datos completos del plan usando InternetPlanSerializer
    plan = InternetPlanSerializer(read_only=True)
     # Agregamos client_id para la creación
    client_id = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        write_only=True,
        source='client'
    )
    # Campo especial para cuando queremos crear/actualizar el servicio
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=InternetPlan.objects.all(),
        write_only=True,# Solo se usa al escribir/crear
        source='plan'  # Se guardará en el campo 'plan' del modelo
    )

    class Meta:
        model = ClientService
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        """
        Validación personalizada para el servicio del cliente.
        """
        if 'installation_date' in data and 'next_payment_date' in data:
            # Comprueba que la fecha de pago no sea anterior a la instalación
            if data['next_payment_date'] < data['installation_date']:
                # Si la fecha es incorrecta, lanza un error
                raise serializers.ValidationError(
                    "Next payment date cannot be before installation date"
                )
        return data