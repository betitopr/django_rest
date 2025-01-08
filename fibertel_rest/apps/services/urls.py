from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# Crear el router
router = DefaultRouter()
# Registrar las rutas
router.register(r'plans', views.InternetPlanViewSet)
router.register(r'client-services', views.ClientServiceViewSet)
# Incluir todas las rutas generadas
urlpatterns = [
    path('', include(router.urls)),
]