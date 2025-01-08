from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Modelo personalizado de usuario que extiende el modelo base de Django.
    Añadimos campos específicos necesarios para el sistema ISP.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    is_client = models.BooleanField(
        _('client status'),
        default=False,
        help_text=_('Designates whether this user is a client.')
    )
    
    # Campos para auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return self.get_full_name() or self.username

class ClientProfile(models.Model):
    
    """
    Perfil extendido para usuarios que son clientes del ISP.
    Contiene información específica necesaria para la gestión del servicio.
    """
    DOCUMENT_CHOICES = [
        ('DNI', 'DNI'),
        ('CE', 'Carnet Extranjería'),
        ('PAS', 'Pasaporte'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    document_type = models.CharField(max_length=3,choices=DOCUMENT_CHOICES,default='DNI')
    document_number = models.CharField(max_length=20)
    address = models.TextField()
    installation_coordinates = models.CharField(max_length=50, blank=True)
    service_status = models.CharField(
        max_length=20,
        choices=[
            ('active', _('Active')),
            ('suspended', _('Suspended')),
            ('cancelled', _('Cancelled'))
        ],
        default='active'
    )
    
    class Meta:
        db_table = 'client_profile'
        verbose_name = _('client profile')
        verbose_name_plural = _('client profiles')

    def __str__(self):
        return f"Profile of {self.user.get_full_name() or self.user.username}"