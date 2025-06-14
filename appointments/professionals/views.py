from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.contrib import messages
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
    
    def form_valid(self, form):
        form.instance.professional_id = self.kwargs['pk']
        form.instance.client = self.request.user
        messages.success(self.request, 'Review added successfully!')
        return super().form_valid(form)

# Professional Dashboard Views (for professionals only)
class ProfessionalDashboardView(LoginRequiredMixin, DetailView):
    """
    Professional dashboard
    """
    model = ProfessionalProfile
    template_name = 'professionals/dashboard.html'
    context_object_name = 'professional'
    
    def get_object(self):
        return get_object_or_404(ProfessionalProfile, user=self.request.user)

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
