from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.services'# Importante: usar el path completo
    verbose_name = 'Services Management'
