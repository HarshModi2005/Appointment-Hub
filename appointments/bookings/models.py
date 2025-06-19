from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from professionals.models import ProfessionalProfile
import uuid

class Appointment(models.Model):
    """
    Appointment booking model
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    APPOINTMENT_TYPES = (
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('urgent', 'Urgent'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES, default='consultation')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True, help_text="Internal notes")
    client_notes = models.TextField(blank=True, help_text="Notes from client")
    professional_notes = models.TextField(blank=True, help_text="Notes from professional")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
        unique_together = ['professional', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.client.get_full_name()} with {self.professional.user.get_full_name()} on {self.date}"
    
    def get_absolute_url(self):
        return reverse('bookings:detail', kwargs={'pk': self.pk})
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.date >= timezone.now().date() and self.status in ['pending', 'confirmed']
    
    @property
    def can_be_cancelled(self):
        from django.utils import timezone
        from datetime import timedelta
        appointment_datetime = timezone.datetime.combine(self.date, self.start_time)
        return appointment_datetime > timezone.now() + timedelta(hours=24)

class TimeSlot(models.Model):
    """
    Available time slots for professionals
    """
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['professional', 'date', 'start_time']
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.professional.user.get_full_name()} - {self.date} {self.start_time}-{self.end_time}"

class AppointmentReminder(models.Model):
    """
    Reminders for appointments
    """
    REMINDER_TYPES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('both', 'Both'),
    )
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=10, choices=REMINDER_TYPES, default='email')
    hours_before = models.PositiveIntegerField(default=24)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['appointment', 'hours_before']
    
    def __str__(self):
        return f"Reminder for {self.appointment} - {self.hours_before}h before"

class Payment(models.Model):
    """
    Payment records for appointments
    """
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_gateway_response = models.JSONField(blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment for {self.appointment} - ₹{self.amount}"
