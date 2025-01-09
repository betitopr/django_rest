from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'tickets', views.TicketViewSet, basename='ticket')

# Rutas anidadas para respuestas de tickets
tickets_router = routers.NestedSimpleRouter(
    router, # Router padre
    r'tickets',  # Prefijo de la ruta padre
    lookup='ticket') # Nombre del parámetro en la URL
tickets_router.register(r'responses', views.TicketResponseViewSet, basename='ticket-responses')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tickets_router.urls)),
]