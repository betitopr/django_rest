from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta
from .models import BandwidthUsage, DailyUsageSummary, MonthlyUsageSummary
from .serializers import (
    BandwidthUsageSerializer,
    DailyUsageSummarySerializer,
    MonthlyUsageSummarySerializer
)

class BandwidthUsageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para monitorear el uso de ancho de banda.
    Solo lectura (ReadOnly) porque los datos se generan automáticamente.
    """
    serializer_class = BandwidthUsageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra los datos según el tipo de usuario:
        - Staff: ve todos los datos
        - Cliente: solo ve sus propios datos
        """
        if self.request.user.is_staff:
            return BandwidthUsage.objects.all()
        return BandwidthUsage.objects.filter(
            service__client=self.request.user
        )

    @action(detail=False, methods=['GET'])
    def last_7_days(self, request):
        """
        Datos para gráfico de los últimos 7 días
        """
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        
        usage = DailyUsageSummary.objects.filter(
            service__client=request.user,
            date__range=[start_date, end_date]
        ).values('date').annotate(
            total_download=Sum('total_download'),
            total_upload=Sum('total_upload')
        ).order_by('date')

        return Response(usage)

    @action(detail=False, methods=['GET'])
    def monthly_summary(self, request):
        """
        Resumen mensual para gráficos
        """
        year = request.query_params.get('year', timezone.now().year)
        data = MonthlyUsageSummary.objects.filter(
            service__client=request.user,
            year=year
        ).order_by('month')
        
        serializer = MonthlyUsageSummarySerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def real_time_usage(self, request):
        """
        Datos de uso en tiempo real (últimas 24 horas)
        """
        last_24h = timezone.now() - timedelta(hours=24)
        usage = BandwidthUsage.objects.filter(
            service__client=request.user,
            timestamp__gte=last_24h
        ).order_by('timestamp')
        
        serializer = self.get_serializer(usage, many=True)
        return Response(serializer.data)