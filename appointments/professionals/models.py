from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class ProfessionalCategory(models.Model):
    """
    Categories for different types of professionals
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    class Meta:
        verbose_name_plural = "Professional Categories"
    
    def __str__(self):
        return self.name

class ProfessionalProfile(models.Model):
    """
    Professional profile for service providers
    """
    EXPERIENCE_CHOICES = (
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5-10', '5-10 years'),
        ('10+', '10+ years'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ProfessionalCategory, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    specializations = models.TextField(help_text="Comma-separated list of specializations")
    bio = models.TextField(max_length=1000, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField()
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='professional_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', '-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.category.name}"
    
    def get_absolute_url(self):
        return reverse('professionals:detail', kwargs={'pk': self.pk})
    
    def get_specializations_list(self):
        return [spec.strip() for spec in self.specializations.split(',') if spec.strip()]

class WorkingHours(models.Model):
    """
    Working hours for professionals
    """
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['professional', 'day_of_week']
        ordering = ['day_of_week']
    
    def __str__(self):
        return f"{self.professional.user.get_full_name()} - {self.get_day_of_week_display()}"

class Review(models.Model):
    """
    Reviews for professionals
    """
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['professional', 'client']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client.get_full_name()} - {self.professional.user.get_full_name()} ({self.rating}/5)"
