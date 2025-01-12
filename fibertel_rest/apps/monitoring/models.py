from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.services.models import ClientService

class BandwidthUsage(models.Model):
    """
    Registro del consumo de ancho de banda por servicio
    """
    # Relación con el servicio del cliente
    service = models.ForeignKey(
        ClientService,
        on_delete=models.CASCADE,
        related_name='bandwidth_usage'
    )
    # Métricas de uso
    # Datos de consumo
    download_usage = models.BigIntegerField( # Bytes descargados
        _('download usage (bytes)'),
        help_text=_('Download usage in bytes')
    )
    upload_usage = models.BigIntegerField(  # Bytes subidos
        _('upload usage (bytes)'),
        help_text=_('Upload usage in bytes')
    )
    
    # Fecha y hora del registro
    timestamp = models.DateTimeField()  # Momento exacto del registro

    
    class Meta:
        db_table = 'bandwidth_usage'
        ordering = ['-timestamp']
        verbose_name = _('bandwidth usage')
        verbose_name_plural = _('bandwidth usage records')
        # Índice compuesto para optimizar consultas
        indexes = [
            models.Index(fields=['service', 'timestamp'])# Para búsquedas rápidas
        ]

    def __str__(self):
        return f"Usage for {self.service} at {self.timestamp}"

class DailyUsageSummary(models.Model):
    """
    Resumen diario de consumo para optimizar consultas
    """
    service = models.ForeignKey(
        ClientService,
        on_delete=models.CASCADE,
        related_name='daily_usage'
    )
     # Totales diarios
    date = models.DateField()# Fecha del resumen
    total_download = models.BigIntegerField()# Total descargado en el día
    total_upload = models.BigIntegerField()# Total subido en el día
    peak_download_speed = models.BigIntegerField()  # Máxima velocidad del día
    peak_upload_speed = models.BigIntegerField()# Velocidad máxima de subida
    average_download_speed = models.BigIntegerField() # Velocidad promedio
    average_upload_speed = models.BigIntegerField()

    class Meta:
        db_table = 'daily_usage_summary'
        ordering = ['-date']
        verbose_name = _('daily usage summary')
        verbose_name_plural = _('daily usage summaries')
        # Asegurar que no haya duplicados
        unique_together = ['service', 'date']

class MonthlyUsageSummary(models.Model):
    """
    Resumen mensual de consumo
    """
    service = models.ForeignKey(
        ClientService,
        on_delete=models.CASCADE,
        related_name='monthly_usage'
    )
    year = models.IntegerField()# Año del resumen
    month = models.IntegerField() # Mes del resumen
    # Totales mensuales
    total_download = models.BigIntegerField()
    total_upload = models.BigIntegerField()
    # Información del pico de uso
    peak_day = models.DateField()# Día de mayor consumo
    peak_download = models.BigIntegerField() # Pico de descarga
    peak_upload = models.BigIntegerField()  # Pico de subida
    # Promedios
    average_daily_download = models.BigIntegerField()# Promedio diario
    average_daily_upload = models.BigIntegerField()

    class Meta:
        db_table = 'monthly_usage_summary'
        ordering = ['-year', '-month']
        unique_together = ['service', 'year', 'month']