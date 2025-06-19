from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from .models import ProfessionalProfile, ProfessionalCategory, Review

class ProfessionalListView(ListView):
    """
    List all professionals
    """
    model = ProfessionalProfile
    template_name = 'professionals/list.html'
    context_object_name = 'professionals'
    paginate_by = 12
    
    def get_queryset(self):
        return ProfessionalProfile.objects.filter(is_available=True).select_related('user', 'category')

class ProfessionalSearchView(ListView):
    """
    Search professionals
    """
    model = ProfessionalProfile
    template_name = 'professionals/search.html'
    context_object_name = 'professionals'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        city = self.request.GET.get('city', '')
        
        queryset = ProfessionalProfile.objects.filter(is_available=True)
        
        if query:
            queryset = queryset.filter(
                user__first_name__icontains=query
            ) | queryset.filter(
                user__last_name__icontains=query
            ) | queryset.filter(
                specializations__icontains=query
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        return queryset.select_related('user', 'category')

class ProfessionalByCategoryView(ListView):
    """
    List professionals by category
    """
    model = ProfessionalProfile
    template_name = 'professionals/by_category.html'
    context_object_name = 'professionals'
    paginate_by = 12
    
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return ProfessionalProfile.objects.filter(
            category_id=category_id,
            is_available=True
        ).select_related('user', 'category')

class ProfessionalDetailView(DetailView):
    """
    Professional detail view
    """
    model = ProfessionalProfile
    template_name = 'professionals/detail.html'
    context_object_name = 'professional'
    
    def get_queryset(self):
        return ProfessionalProfile.objects.select_related('user', 'category').prefetch_related('reviews')

class BookAppointmentView(LoginRequiredMixin, DetailView):
    """
    Book appointment with professional
    """
    model = ProfessionalProfile
    template_name = 'professionals/book.html'
    context_object_name = 'professional'
    
    def post(self, request, *args, **kwargs):
        """Handle appointment booking form submission"""
        from bookings.models import Appointment
        from datetime import datetime
        
        # Get the professional
        professional = self.get_object()
        
        # Get form data
        appointment_type = request.POST.get('appointment_type', 'consultation')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        subject = request.POST.get('subject')
        description = request.POST.get('description', '')
        
        # Basic validation
        if not all([date, start_time, end_time, subject]):
            messages.error(request, 'Please fill in all required fields.')
            return self.get(request, *args, **kwargs)
        
        # Calculate duration in minutes
        duration_minutes = 60  # Default
        if start_time and end_time:
            try:
                start_dt = datetime.strptime(start_time, '%H:%M')
                end_dt = datetime.strptime(end_time, '%H:%M')
                duration_delta = end_dt - start_dt
                if duration_delta.total_seconds() <= 0:
                    messages.error(request, 'End time must be after start time.')
                    return self.get(request, *args, **kwargs)
                duration_minutes = int(duration_delta.total_seconds() / 60)
            except ValueError:
                messages.error(request, 'Invalid time format.')
                return self.get(request, *args, **kwargs)
        
        # Create appointment from form data
        appointment = Appointment(
            client=request.user,
            professional=professional,
            appointment_type=appointment_type,
            date=date,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_minutes,
            subject=subject,
            description=description,
            fee=professional.consultation_fee
        )
        
        try:
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('bookings:detail', pk=appointment.pk)
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
            return self.get(request, *args, **kwargs)

class ProfessionalReviewsView(DetailView):
    """
    Professional reviews view
    """
    model = ProfessionalProfile
    template_name = 'professionals/reviews.html'
    context_object_name = 'professional'

class AddReviewView(LoginRequiredMixin, CreateView):
    """
    Add review for professional
    """
    model = Review
    fields = ['rating', 'comment']
    template_name = 'professionals/add_review.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(ProfessionalProfile, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        professional = get_object_or_404(ProfessionalProfile, pk=self.kwargs['pk'])
        form.instance.professional = professional
        form.instance.client = self.request.user
        messages.success(self.request, 'Review added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('professionals:reviews', kwargs={'pk': self.kwargs['pk']})

# Professional Dashboard Views (for professionals only)
class ProfessionalDashboardView(LoginRequiredMixin, DetailView):
    """
    Professional dashboard
    """
    model = ProfessionalProfile
    template_name = 'professionals/dashboard.html'
    context_object_name = 'professional'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has a UserProfile with professional type
        try:
            user_profile = request.user.userprofile
            if user_profile.user_type != 'professional':
                # Redirect non-professionals to home page
                messages.error(request, 'Access denied. Professional account required.')
                return redirect('home')
        except:
            # User doesn't have a UserProfile, redirect to home
            messages.error(request, 'Please complete your profile setup.')
            return redirect('home')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        # Try to get existing ProfessionalProfile, create if doesn't exist
        try:
            return ProfessionalProfile.objects.get(user=self.request.user)
        except ProfessionalProfile.DoesNotExist:
            # Create a basic ProfessionalProfile for professionals who don't have one yet
            from .models import ProfessionalCategory
            
            # Get or create a default category
            default_category, created = ProfessionalCategory.objects.get_or_create(
                name='General Consultant',
                defaults={'description': 'General consulting services'}
            )
            
            # Create ProfessionalProfile with proper default values for required fields
            professional_profile = ProfessionalProfile.objects.create(
                user=self.request.user,
                category=default_category,
                experience='0-1',  # Default value
                specializations='General consulting',  # Default value
                hourly_rate=50.00,  # Default value
                consultation_fee=100.00,  # Default value
                phone='000-000-0000',  # Default placeholder phone
                city='Not specified',   # Default city
                state='Not specified',  # Default state
                address='Please update your address',  # Default address with meaningful text
                bio='Please update your professional information.',
            )
            
            messages.info(self.request, 'Professional profile created. Please update your information.')
            return professional_profile

class ProfessionalProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Professional profile edit
    """
    model = ProfessionalProfile
    fields = ['category', 'business_name', 'license_number', 'experience', 
              'specializations', 'bio', 'hourly_rate', 'consultation_fee',
              'phone', 'city', 'state', 'address', 'website', 'linkedin']
    template_name = 'professionals/profile_edit.html'
    
    def get_object(self):
        return get_object_or_404(ProfessionalProfile, user=self.request.user)

class ProfessionalScheduleView(LoginRequiredMixin, DetailView):
    """
    Professional schedule management
    """
    model = ProfessionalProfile
    template_name = 'professionals/schedule.html'
    context_object_name = 'professional'
    
    def get_object(self):
        return get_object_or_404(ProfessionalProfile, user=self.request.user)

class ProfessionalAppointmentsView(LoginRequiredMixin, DetailView):
    """
    Professional appointments view
    """
    model = ProfessionalProfile
    template_name = 'professionals/appointments.html'
    context_object_name = 'professional'
    
    def get_object(self):
        return get_object_or_404(ProfessionalProfile, user=self.request.user)

class ProfessionalReviewsManageView(LoginRequiredMixin, DetailView):
    """
    Professional reviews management
    """
    model = ProfessionalProfile
    template_name = 'professionals/reviews_manage.html'
    context_object_name = 'professional'
    
    def get_object(self):
        return get_object_or_404(ProfessionalProfile, user=self.request.user)

# AJAX Views
def get_available_slots(request):
    """
    Get available time slots for a professional
    """
    # Placeholder implementation
    return JsonResponse({'slots': []})

def update_availability(request):
    """
    Update professional availability
    """
    # Placeholder implementation
    return JsonResponse({'success': True})
