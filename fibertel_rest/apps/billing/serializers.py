from rest_framework import serializers
from .models import Invoice, Payment
from apps.accounts.serializers import UserSerializer
from apps.services.serializers import ClientServiceSerializer
from apps.services.models import ClientService
from apps.accounts.models import User

class InvoiceSerializer(serializers.ModelSerializer):
    # Muestra datos completos del cliente y servicio al leer (GET)
    client = UserSerializer(read_only=True)
    service = ClientServiceSerializer(read_only=True)

    # Solo acepta IDs al crear/actualizar (POST/PUT)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='client'# Mapea client_id al campo client del modelo
    )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=ClientService.objects.all(),
        write_only=True,
        source='service'
    )

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


    # Valida que la fecha de vencimiento sea posterior a la de emisión
    def validate(self, data): 
        if 'due_date' in data and 'issue_date' in data:
            if data['due_date'] < data['issue_date']:
                raise serializers.ValidationError(
                    "Due date cannot be before issue date"
                )
        
        # Nueva validación de consistencia cliente-servicio
        if 'client' in data and 'service' in data:
            if data['service'].client != data['client']:
                raise serializers.ValidationError(
                    "The service must belong to the specified client"
                )
                
        return data
    


class PaymentSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)# Muestra factura completa en GET
    invoice_id = serializers.PrimaryKeyRelatedField( 
        queryset=Invoice.objects.all(),
        write_only=True,
        source='invoice'
    )

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')