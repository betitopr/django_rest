from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Ticket, TicketResponse
from .serializers import TicketSerializer, TicketResponseSerializer

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]#Solo permite usuarios autenticados

    def get_queryset(self):
         # Si es staff ve todos los tickets, si no, solo los suyos
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(client=self.request.user)
    
    def perform_create(self, serializer):
        """
        Asigna automáticamente el cliente actual al ticket
        """
        serializer.save(client=self.request.user)
    
    def get_serializer_context(self):
        """
        Pasa el usuario actual al serializer
        """
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    #Acciones personalizadas

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        # Accion para marcar al ticket resuelto
        ticket = self.get_object()
        ticket.status = 'resolved'
        ticket.resolution_date = timezone.now()
        ticket.resolution = request.data.get('resolution', '')
        ticket.save()
        return Response({'status': 'ticket resolved'})

    @action(detail=True, methods=['post'])
      # Accion para marcar al ticket como reabrir
    def reopen(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = 'open'
        ticket.save()
        return Response({'status': 'ticket reopened'})
    
    def validate(self, data):
        """
        Valida que el servicio pertenezca al cliente que crea el ticket
        """
        client = data.get('client')
        service = data.get('service')

        if client and service:
            # Verifica si el servicio pertenece al cliente
            if service.client != client:
                raise serializers.ValidationError({
                    'service': 'Este servicio no pertenece al cliente especificado.'
                })
        
        return data
    


class TicketResponseViewSet(viewsets.ModelViewSet):

    serializer_class = TicketResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtra las respuestas por ticket específico
        return TicketResponse.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
         # Al crear una respuesta, asigna automáticamente al ticket y usuario:
        ticket = Ticket.objects.get(pk=self.kwargs['ticket_pk'])
        serializer.save(
            ticket=ticket,
            user=self.request.user,
            is_staff_response=self.request.user.is_staff
        )