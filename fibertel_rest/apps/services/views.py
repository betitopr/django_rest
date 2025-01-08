from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InternetPlan, ClientService
from .serializers import InternetPlanSerializer, ClientServiceSerializer

class InternetPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar planes de internet.(Solo para admins)
    """
    queryset = InternetPlan.objects.all()
    serializer_class = InternetPlanSerializer
    permission_classes = [permissions.IsAdminUser]# Solo admins por defecto

    def get_permissions(self):
        if self.action in ['list', 'retrieve']: # Si es para ver planes
            return [permissions.IsAuthenticated()] # Solo requiere estar logueado
        return super().get_permissions()# Para otras acciones, requiere ser admin

class ClientServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar servicios de clientes.
    """
    queryset = ClientService.objects.all()
    serializer_class = ClientServiceSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:# Si es admin
            return ClientService.objects.all()# Ve todos los servicios
        # Si es cliente normal, solo ve su propio servicio
        return ClientService.objects.filter(client=self.request.user)

     # Acciones especiales para suspender o activar un servicio
     
    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        service = self.get_object()# Obtiene el servicio
        service.status = 'suspended' # Cambia su estado
        service.save()
        return Response({'status': 'service suspended'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        service = self.get_object()
        service.status = 'active'
        service.save()
        return Response({'status': 'service activated'})