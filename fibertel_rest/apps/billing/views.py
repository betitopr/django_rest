from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar facturas con permisos diferenciados:
    - Staff: Acceso total a todas las facturas
    - Clientes: Solo acceso a sus propias facturas
    """
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]# Solo usuarios autenticados

    def get_queryset(self):
        # Staff ve todas las facturas, clientes solo las suyas
        if self.request.user.is_staff:
            return Invoice.objects.all()
        return Invoice.objects.filter(client=self.request.user)
      # Acciones personalizadas

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        # Marca factura como pagada
        invoice = self.get_object()
        invoice.status = 'paid'
        invoice.save()
        return Response({'status': 'invoice marked as paid'})

    @action(detail=True, methods=['post'])
    def mark_as_overdue(self, request, pk=None):
         # Marca factura como vencida
        invoice = self.get_object()
        invoice.status = 'overdue'
        invoice.save()
        return Response({'status': 'invoice marked as overdue'})

class PaymentViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar pagos:
    - Staff: Ve todos los pagos
    - Clientes: Solo ven pagos de sus facturas
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(invoice__client=self.request.user)