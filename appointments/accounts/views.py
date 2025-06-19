from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UserProfile

# Create your views here.

class SignUpView(CreateView):
    """
    User registration view
    """
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Create user profile
        UserProfile.objects.create(
            user=self.object,
            user_type='client'
        )
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class ProfessionalSignUpView(CreateView):
    """
    Professional registration view
    """
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/professional_signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Create professional user profile
        UserProfile.objects.create(
            user=self.object,
            user_type='professional'
        )
        
        # Also create a basic ProfessionalProfile
        from professionals.models import ProfessionalProfile, ProfessionalCategory
        
        # Get or create a default category
        default_category, created = ProfessionalCategory.objects.get_or_create(
            name='General Consultant',
            defaults={
                'description': 'General consulting services',
                'icon': 'fas fa-user-tie'
            }
        )
        
        # Create ProfessionalProfile with proper default values for required fields
        ProfessionalProfile.objects.create(
            user=self.object,
            category=default_category,
            experience='0-1',  # Default value
            specializations='General consulting',  # Default value
            hourly_rate=50.00,  # Default value
            consultation_fee=100.00,  # Default value
            phone='000-000-0000',  # Default placeholder phone
            city='Not specified',   # Default city
            state='Not specified',  # Default state
            address='Please update your address',  # Default value since it's required
            bio='Please update your professional information.',
        )
        
        messages.success(self.request, 'Professional account created successfully! Please log in and complete your profile.')
        return response

class ProfileView(LoginRequiredMixin, DetailView):
    """
    User profile view
    """
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'user_type': 'client'}
        )
        return profile

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    User profile edit view
    """
    model = UserProfile
    fields = ['phone', 'city', 'state', 'address', 'profile_picture']
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'user_type': 'client'}
        )
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class CustomLogoutView(auth_views.LogoutView):
    """
    Custom logout view with success message
    """
    next_page = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)
