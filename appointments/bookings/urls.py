from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Client booking management
    path('', views.AppointmentListView.as_view(), name='list'),
    path('my-appointments/', views.MyAppointmentsView.as_view(), name='my_appointments'),
    path('<uuid:pk>/', views.AppointmentDetailView.as_view(), name='detail'),
    path('<uuid:pk>/cancel/', views.CancelAppointmentView.as_view(), name='cancel'),
    path('<uuid:pk>/reschedule/', views.RescheduleAppointmentView.as_view(), name='reschedule'),
    
    # Booking process
    path('book/<int:professional_id>/', views.BookAppointmentView.as_view(), name='book'),
    path('book/<int:professional_id>/confirm/', views.ConfirmBookingView.as_view(), name='confirm'),
    path('booking-success/<uuid:appointment_id>/', views.BookingSuccessView.as_view(), name='success'),
    
    # Payment
    path('<uuid:pk>/payment/', views.PaymentView.as_view(), name='payment'),
    path('<uuid:pk>/payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('<uuid:pk>/payment/failed/', views.PaymentFailedView.as_view(), name='payment_failed'),
    
    # AJAX endpoints
    path('ajax/check-availability/', views.check_availability, name='check_availability'),
    path('ajax/get-time-slots/', views.get_time_slots, name='get_time_slots'),
] 