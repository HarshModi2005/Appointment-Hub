from django.contrib import admin
from .models import Appointment, TimeSlot, AppointmentReminder, Payment

class AppointmentReminderInline(admin.TabularInline):
    model = AppointmentReminder
    extra = 1

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['client', 'professional', 'date', 'start_time', 'status', 'fee', 'is_paid']
    list_filter = ['status', 'appointment_type', 'date', 'is_paid', 'created_at']
    search_fields = ['client__username', 'client__first_name', 'client__last_name', 
                    'professional__user__username', 'professional__user__first_name', 
                    'professional__user__last_name', 'subject']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'cancelled_at']
    inlines = [AppointmentReminderInline, PaymentInline]
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('id', 'client', 'professional', 'appointment_type', 'subject', 'description')
        }),
        ('Schedule', {
            'fields': ('date', 'start_time', 'end_time', 'duration_minutes')
        }),
        ('Status & Payment', {
            'fields': ('status', 'fee', 'is_paid', 'payment_method')
        }),
        ('Notes', {
            'fields': ('notes', 'client_notes', 'professional_notes'),
            'classes': ('collapse',)
        }),
        ('Cancellation', {
            'fields': ('cancellation_reason',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'cancelled_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('client', 'professional__user')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['professional', 'date', 'start_time', 'end_time', 'is_available', 'is_blocked']
    list_filter = ['is_available', 'is_blocked', 'date']
    search_fields = ['professional__user__username', 'professional__user__first_name', 'professional__user__last_name']
    readonly_fields = ['created_at']

@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'reminder_type', 'hours_before', 'is_sent', 'sent_at']
    list_filter = ['reminder_type', 'is_sent', 'hours_before']
    readonly_fields = ['sent_at', 'created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'amount', 'payment_method', 'status', 'paid_at']
    list_filter = ['payment_method', 'status', 'paid_at', 'created_at']
    search_fields = ['appointment__client__username', 'transaction_id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'paid_at']
