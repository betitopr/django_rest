from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class InternetPlan(models.Model):
    """
    Modelo para los planes de internet disponibles en el ISP.
    """
    name = models.CharField(_('plan name'), max_length=100)# Nombre del plan (ej: "Plan Fibra 100MB")
    download_speed = models.IntegerField(_('download speed (Mbps)'))# Velocidad de descarga
    upload_speed = models.IntegerField(_('upload speed (Mbps)')) # Velocidad de subida
    price = models.DecimalField(_('monthly price'), max_digits=10, decimal_places=2)# Precio mensual
    description = models.TextField(_('description'))# Descripción detallada del plan
    is_active = models.BooleanField(_('active'), default=True)# Si el plan está disponible
    
    # Campos de auditoría(automaticos)
    created_at = models.DateTimeField(auto_now_add=True) # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última modificación

    class Meta:
        db_table = 'internet_plans'# Nombre de la tabla en la base de datos
        verbose_name = _('internet plan')
        verbose_name_plural = _('internet plans')
        ordering = ['price']

    def __str__(self):
        return f"{self.name} - {self.download_speed}Mbps"

class ClientService(models.Model):
    """
    Modelo para gestionar los servicios asignados a clientes.
    """
    #Opciones de estado del servicio
    STATUS_CHOICES = [
        ('active', _('Active')),  # Servicio activo
        ('suspended', _('Suspended')),# Servicio suspendido (ej: por falta de pago)
        ('cancelled', _('Cancelled')),# Servicio cancelado
    ]

    client = models.ForeignKey( # Relación con el modelo User
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='internet_services' # Acceso desde user: user.internet_service
    )
    plan = models.ForeignKey( 
        InternetPlan, # Relación con el plan de internet
        on_delete=models.PROTECT, # No permite eliminar un plan si tiene clientes
        related_name='subscriptions' # Acceso desde plan: plan.subscriptions.all()
    )

    #Campos del servicio
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    installation_date = models.DateField()
    ip_address = models.GenericIPAddressField(
        protocol='IPv4',
        null=True,
        blank=True
    )
    mac_address = models.CharField(
        max_length=17,
        blank=True,
        null=True
    )
     # Campos de facturación
    last_payment_date = models.DateField(null=True, blank=True)
    next_payment_date = models.DateField()
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client_services'
        verbose_name = _('client service')
        verbose_name_plural = _('client services')

    def __str__(self):
        return f"Service for {self.client.get_full_name()} - {self.plan.name}"
