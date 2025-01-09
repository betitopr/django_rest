from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
     # Lista de facturas muestra información clave
    list_display = ('invoice_number', 'client', 'amount', 'status', 'issue_date', 'due_date')
     # Filtros útiles para gestión
    list_filter = ('status', 'issue_date')
    search_fields = ('invoice_number', 'client__email', 'client__username')
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('invoice_number', 'client', 'service')
        }),
        ('Financial Details', {
            'fields': ('amount', 'subtotal', 'tax')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date')
        }),
        ('Status', {
            'fields': ('status', 'description')
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Campos relevantes para seguimiento de pagos
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method', 'transaction_id')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('transaction_id', 'invoice__invoice_number')
    date_hierarchy = 'payment_date'