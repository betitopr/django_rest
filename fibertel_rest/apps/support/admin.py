from django.contrib import admin
from .models import Ticket, TicketResponse

@admin.register(Ticket)#Regitramos el modelo Ticket
class TicketAdmin(admin.ModelAdmin):
        #Columnas que se muetran en la lista de tickets
    list_display = (
        'ticket_number',
        'client',
        'title',
        'status',
        'priority',
        'created_at'
    )
     # Filtros en la barra lateral
    list_filter = ('status', 'priority', 'category')
    # Campos de búsqueda
    search_fields = (
        'ticket_number',
        'client__email',
        'title',
        'description'
    )
    # Campos de solo lectura
    readonly_fields = ('ticket_number', 'created_at', 'updated_at')

@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
    # Columnas en la lista de respuestass
    list_display = ('ticket', 'user', 'is_staff_response', 'created_at')
     # Filtros en la barra lateral
    list_filter = ('is_staff_response', 'created_at')
      # Campos por los que se puede buscar
    search_fields = ('ticket__ticket_number', 'message')