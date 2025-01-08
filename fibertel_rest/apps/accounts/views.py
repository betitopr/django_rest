from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import ClientProfile
from .serializers import (
    UserSerializer, 
    ClientProfileSerializer,
    ISPTokenObtainPairSerializer
)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista personalizada para obtener tokens JWT"""
    serializer_class = ISPTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en usuarios
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()# Admin ve todos
        return User.objects.filter(id=self.request.user.id)# Usuario normal solo se ve a sí mismo

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Endpoint para obtener datos del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ClientProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en perfiles de cliente
    """
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ClientProfile.objects.all()
        return ClientProfile.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Crear perfil de cliente con usuario asociado"""
        # Asegurarnos de que se proporcione un usuario
        if 'user_id' not in request.data:
            return Response(
                {"error": "Se requiere un usuario para crear un perfil"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
         # Verificar si el usuario existe
        try:
            User.objects.get(id=request.data['user_id'])
        except User.DoesNotExist:
            return Response(
                {"error": f"No existe usuario con ID {request.data['user_id']}"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)#Devuelve un objeto serializador con los datos envidados
        
        if serializer.is_valid():#Validar datos
            self.perform_create(serializer) #Guardar perfil en la BD
            headers = self.get_success_headers(serializer.data)#Prepara los encabezados de respuesta
            return Response( #Devuelve la respuesta con el perfil
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
