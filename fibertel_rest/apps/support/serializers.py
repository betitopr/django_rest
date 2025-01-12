from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ticket, TicketResponse,ClientService
from apps.accounts.serializers import UserSerializer
from apps.services.serializers import ClientServiceSerializer

User = get_user_model()

class TicketResponseSerializer(serializers.ModelSerializer):
    # Incluimos informacion completa del usuario ligado al ticket
    user = UserSerializer(read_only=True)

    class Meta:
        model = TicketResponse
        fields = '__all__'
        read_only_fields = ('is_staff_response', 'created_at')

class TicketSerializer(serializers.ModelSerializer):
    #Campos de solo lectura (Mostramos toda la informacion completa)
    client = UserSerializer(read_only=True)
    service = ClientServiceSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    responses = TicketResponseSerializer(many=True, read_only=True)
    
    # Campos para escritura (Solo aceptamos IDs)
    # client_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     write_only=True,
    #     source='client'
    # )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=ClientService.objects.all(),
        write_only=True,
        source='service'
    )
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True),# Solo staff puede ser asignado
        write_only=True,
        source='assigned_to',
        required=False# Es opcional
    )

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('ticket_number', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Generar número de ticket automáticamente
        last_ticket = Ticket.objects.order_by('-id').first()
        ticket_num = f"TKT-{s(last_ticket.id + 1 if last_ticket else 1):06d}"
        validated_data['ticket_number'] = ticket_num
        
        # Asignar el cliente actual
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)

    
    def validate_service_id(self, value):
        """
        Valida que el servicio pertenezca al usuario autenticado
        """
        user = self.context['request'].user
        if not user.is_staff and value.client != user:
            raise serializers.ValidationError(
                'Solo puede crear tickets para sus propios servicios.'
            )
        return value