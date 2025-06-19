from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Appointment, Payment
from professionals.models import ProfessionalProfile

class AppointmentListView(LoginRequiredMixin, ListView):
    """
    List all appointments (admin view)
    """
    model = Appointment
    template_name = 'bookings/list.html'
    context_object_name = 'appointments'
    paginate_by = 20
    
    def get_queryset(self):
        return Appointment.objects.select_related('client', 'professional__user')

class MyAppointmentsView(LoginRequiredMixin, ListView):
    """
    User's appointments view
    """
    model = Appointment
    template_name = 'bookings/my_appointments.html'
    context_object_name = 'appointments'
    paginate_by = 10
    
    def get_queryset(self):
        return Appointment.objects.filter(
            client=self.request.user
        ).select_related('professional__user').order_by('-date', '-start_time')

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    """
    Appointment detail view
    """
    model = Appointment
    template_name = 'bookings/detail.html'
    context_object_name = 'appointment'
    
    def get_queryset(self):
        return Appointment.objects.select_related('client', 'professional__user')

class CancelAppointmentView(LoginRequiredMixin, UpdateView):
    """
    Cancel appointment view
    """
    model = Appointment
    fields = ['cancellation_reason']
    template_name = 'bookings/cancel.html'
    
    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user)
    
    def form_valid(self, form):
        form.instance.status = 'cancelled'
        messages.success(self.request, 'Appointment cancelled successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('bookings:my_appointments')

class RescheduleAppointmentView(LoginRequiredMixin, UpdateView):
    """
    Reschedule appointment view
    """
    model = Appointment
    fields = ['date', 'start_time', 'end_time']
    template_name = 'bookings/reschedule.html'
    
    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user)
    
    def form_valid(self, form):
        form.instance.status = 'pending'  # Reset to pending after reschedule
        messages.success(self.request, 'Appointment rescheduled successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('bookings:detail', kwargs={'pk': self.object.pk})

class BookAppointmentView(LoginRequiredMixin, CreateView):
    """
    Book new appointment view
    """
    model = Appointment
    fields = ['appointment_type', 'date', 'start_time', 'end_time', 'subject', 'description']
    template_name = 'bookings/book.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['professional'] = get_object_or_404(
            ProfessionalProfile, 
            pk=self.kwargs['professional_id']
        )
        return context
    
    def form_valid(self, form):
        professional = get_object_or_404(
            ProfessionalProfile, 
            pk=self.kwargs['professional_id']
        )
        form.instance.client = self.request.user
        form.instance.professional = professional
        form.instance.fee = professional.consultation_fee
        messages.success(self.request, 'Appointment booked successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('bookings:detail', kwargs={'pk': self.object.pk})

class ConfirmBookingView(LoginRequiredMixin, DetailView):
    """
    Confirm booking details view
    """
    model = Appointment
    template_name = 'bookings/confirm.html'
    context_object_name = 'appointment'

class BookingSuccessView(LoginRequiredMixin, DetailView):
    """
    Booking success view
    """
    model = Appointment
    template_name = 'bookings/success.html'
    context_object_name = 'appointment'
    
    def get_object(self):
        return get_object_or_404(Appointment, pk=self.kwargs['appointment_id'])

class PaymentView(LoginRequiredMixin, DetailView):
    """
    Payment view for appointment
    """
    model = Appointment
    template_name = 'bookings/payment.html'
    context_object_name = 'appointment'
    
    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user)

class PaymentSuccessView(LoginRequiredMixin, DetailView):
    """
    Payment success view
    """
    model = Appointment
    template_name = 'bookings/payment_success.html'
    context_object_name = 'appointment'
    
    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user)

class PaymentFailedView(LoginRequiredMixin, DetailView):
    """
    Payment failed view
    """
    model = Appointment
    template_name = 'bookings/payment_failed.html'
    context_object_name = 'appointment'
    
    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user)

# AJAX Views
def check_availability(request):
    """
    Check availability for a specific date and time
    """
    # Placeholder implementation
    return JsonResponse({'available': True})

def get_time_slots(request):
    """
    Get available time slots for a professional on a specific date
    """
    # Placeholder implementation
    return JsonResponse({'slots': []})
