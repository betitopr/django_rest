from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.services.models import ClientService

class Ticket(models.Model):
    """
    Modelo para gestionar tickets de soporte técnico
    """
    PRIORITY_CHOICES = [
        ('low', _('Low')),      # Prioridad baja
        ('medium', _('Medium')),   # Prioridad media 
        ('high', _('High')),    # Prioridad alta
        ('urgent', _('Urgent')), # Prioridad urgente
    ]
    
    STATUS_CHOICES = [
        ('open', _('Open')),    # Ticket abierto
        ('in_progress', _('In Progress')),  # En proceso
        ('waiting', _('Waiting for Client')),   # Esperando respuesta del cliente
        ('resolved', _('Resolved')),     # Resuelto
        ('closed', _('Closed')),     # Cerrado
    ]

    CATEGORY_CHOICES = [
        ('technical', _('Technical Issue')),# Problemas técnicos
        ('billing', _('Billing Issue')), # Problemas de facturación
        ('speed', _('Speed Problem')),# Problemas de velocidad
        ('connection', _('Connection Problem')),# Problemas de conexión
        ('installation', _('Installation')),# Instalaciones
        ('other', _('Other')),
    ]

    # Relaciones
    client = models.ForeignKey( # Usuario que creó el ticket
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    service = models.ForeignKey( # Servicio relacionado al ticket
        ClientService,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    assigned_to = models.ForeignKey(# Técnico asignado
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    # Campos del ticket
    ticket_number = models.CharField(max_length=20, unique=True)# Número único del ticket
    title = models.CharField(max_length=200) # Título del ticket
    description = models.TextField() # Descripción detallada
    category = models.CharField( # Categoría del problema
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='technical'
    )
    priority = models.CharField(# Prioridad del ticket
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField( # Estado actual
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    # Campos de seguimiento
    resolution = models.TextField(blank=True) # Descripción de la resolución
    resolution_date = models.DateTimeField(null=True, blank=True)# Fecha de resolución
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'support_tickets'
        ordering = ['-created_at']
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.client.get_full_name()}"

class TicketResponse(models.Model):
    """
    Modelo para gestionar respuestas/comentarios en tickets
    """
    ticket = models.ForeignKey(# Ticket al que pertenece la respuesta
        Ticket,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    user = models.ForeignKey(# Usuario que respondió
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_responses'
    )
    message = models.TextField() # Contenido de la respuesta
    is_staff_response = models.BooleanField(default=False)# Indica si es respuesta del staff
    attachment = models.FileField(# Archivos adjuntos
        upload_to='ticket_attachments/%Y/%m/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_responses'
        ordering = ['created_at']
        verbose_name = _('ticket response')
        verbose_name_plural = _('ticket responses')

    def __str__(self):
        return f"Response to ticket #{self.ticket.ticket_number}"