from rest_framework import serializers
from .models import BandwidthUsage, DailyUsageSummary, MonthlyUsageSummary

class BandwidthUsageSerializer(serializers.ModelSerializer):
    """
    Serializer para el consumo de ancho de banda instantáneo.
    Convierte los datos almacenados en bytes a megabytes para mejor lectura.
    """
    # Campos calculados que mostrarán el consumo en megabytes
    download_mb = serializers.SerializerMethodField()
    upload_mb = serializers.SerializerMethodField()

    class Meta:
        model = BandwidthUsage
        fields = '__all__'
    
    # Métodos para convertir bytes a megabytes Mb
    def get_download_mb(self, obj):
        """
        Convierte los bytes de descarga a megabytes
        1 MB = 1024 * 1024 bytes (1024 KB * 1024 = 1 MB)
        """
        return round(obj.download_usage / (1024 * 1024), 2)

    def get_upload_mb(self, obj):
        """
        Convierte los bytes de subida a megabytes
        Redondea el resultado a 2 decimales para mejor presentación
        """
        return round(obj.upload_usage / (1024 * 1024), 2)

class DailyUsageSummarySerializer(serializers.ModelSerializer):
    """
    Serializer para el resumen diario de consumo.
    Convierte los totales diarios de bytes a gigabytes.
    """
    # Campos calculados para mostrar el consumo diario en GB
    download_gb = serializers.SerializerMethodField()
    upload_gb = serializers.SerializerMethodField()
    
    class Meta:
        model = DailyUsageSummary
        fields = '__all__'
    # Métodos para convertir bytes a gigabytes
    def get_download_gb(self, obj):
        return round(obj.total_download / (1024 * 1024 * 1024), 2)

    def get_upload_gb(self, obj):
        return round(obj.total_upload / (1024 * 1024 * 1024), 2)

class MonthlyUsageSummarySerializer(serializers.ModelSerializer):
    """
    Serializer para el resumen mensual de consumo.
    Agrega el nombre del mes y convierte los totales a gigabytes.
    """
    month_name = serializers.SerializerMethodField()
    total_download_gb = serializers.SerializerMethodField()
    total_upload_gb = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyUsageSummary
        fields = '__all__'

    def get_month_name(self, obj):
        return {
            1: 'January', 2: 'February', 3: 'March',
            4: 'April', 5: 'May', 6: 'June',
            7: 'July', 8: 'August', 9: 'September',
            10: 'October', 11: 'November', 12: 'December'
        }[obj.month]

    def get_total_download_gb(self, obj):
        return round(obj.total_download / (1024 * 1024 * 1024), 2)

    def get_total_upload_gb(self, obj):
        return round(obj.total_upload / (1024 * 1024 * 1024), 2)