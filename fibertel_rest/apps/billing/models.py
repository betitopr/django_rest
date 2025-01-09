from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.services.models import ClientService

class Invoice(models.Model):
    """
    Modelo para facturas de servicios de internet con los siguientes componentes principales:
    - Relaciones con Cliente y Servicio
    - Información de facturación (número, monto, fechas)
    - Estado del pago
    - Detalles financieros (subtotal, impuestos)
    """
    # Estados posibles de pago para la factura
    PAYMENT_STATUS = [
        ('pending', _('Pending')),  # Factura emitida pero no pagada
        ('paid', _('Paid')),       # Factura pagada completamente
        ('overdue', _('Overdue')), # Factura vencida sin pago
        ('cancelled', _('Cancelled')), # Factura cancelada/anulada
    ]
    # Relación con el modelo de Usuario (Cliente)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invoices'# Permite acceder como: cliente.invoices.all()
    )
     # Relación con el servicio contratado
      # PROTECT: No permite eliminar un servicio si tiene facturas asociadas
    service = models.ForeignKey(
        ClientService,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    invoice_number = models.CharField(max_length=50, unique=True)#Numero de factura
    amount = models.DecimalField(max_digits=10, decimal_places=2)#cantidad
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending' # Estado inicial al crear factura
    )
    issue_date = models.DateField()#Fecha de emision
    due_date = models.DateField()#Fecha de vencimiento
    
    # Campos opcionales para detalles adicionales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2) 
    tax = models.DecimalField(max_digits=10, decimal_places=2) #Impuesto
    description = models.TextField(blank=True) #Descripcion
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'invoices'
        ordering = ['-issue_date']
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.client.get_full_name()}"

class Payment(models.Model):
    """
    Modelo para registrar pagos individuales asociados a facturas.
    Permite:
    - Registrar pagos parciales o totales
    - Diferentes métodos de pago
    - Almacenar comprobantes
    """
    # Métodos de pago disponibles
    PAYMENT_METHODS = [
        ('cash', _('Cash')),
        ('credit_card', _('Credit Card')),
        ('bank_transfer', _('Bank Transfer')),
        ('digital_wallet', _('Digital Wallet')),
    ]
    # Relación con la factura
     # PROTECT: No permite eliminar una factura si tiene pagos registrados
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name='payments'# Permite: factura.payments.all()
    )

    #Informacion del Pago
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField() #Fecha de pago
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)#Metodo de pago
    transaction_id = models.CharField(max_length=100, blank=True)#transaccion
    
    # Almacenamiento del comprobante
    payment_proof = models.FileField(
        upload_to='payment_proofs/%Y/%m/',  # Organiza por año/mes
        null=True,
        blank=True
    )
    
    notes = models.TextField(blank=True)
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-payment_date']
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def __str__(self):
        return f"Payment {self.id} for Invoice #{self.invoice.invoice_number}"