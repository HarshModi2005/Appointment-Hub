from django.contrib import admin
from .models import ProfessionalCategory, ProfessionalProfile, WorkingHours, Review

@admin.register(ProfessionalCategory)
class ProfessionalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name']

class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 7
    max_num = 7

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['client', 'rating', 'comment', 'created_at']

@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'city', 'state', 'hourly_rate', 'rating', 'is_verified', 'is_available']
    list_filter = ['category', 'city', 'state', 'is_verified', 'is_available', 'experience']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'business_name']
    readonly_fields = ['rating', 'total_reviews', 'created_at', 'updated_at']
    inlines = [WorkingHoursInline, ReviewInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'category', 'business_name', 'license_number')
        }),
        ('Professional Details', {
            'fields': ('experience', 'specializations', 'bio', 'hourly_rate', 'consultation_fee')
        }),
        ('Contact Information', {
            'fields': ('phone', 'city', 'state', 'address', 'website', 'linkedin')
        }),
        ('Status & Rating', {
            'fields': ('is_verified', 'is_available', 'rating', 'total_reviews')
        }),
        ('Media', {
            'fields': ('profile_picture',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ['professional', 'get_day_of_week_display', 'start_time', 'end_time', 'is_available']
    list_filter = ['day_of_week', 'is_available']
    search_fields = ['professional__user__username', 'professional__user__first_name', 'professional__user__last_name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['professional', 'client', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['professional__user__username', 'client__username', 'comment']
    readonly_fields = ['created_at']
