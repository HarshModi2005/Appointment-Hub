from django.urls import path
from . import views

app_name = 'professionals'

urlpatterns = [
    # Professional listing and search
    path('', views.ProfessionalListView.as_view(), name='list'),
    path('search/', views.ProfessionalSearchView.as_view(), name='search'),
    path('category/<int:category_id>/', views.ProfessionalByCategoryView.as_view(), name='by_category'),
    
    # Professional detail and booking
    path('<int:pk>/', views.ProfessionalDetailView.as_view(), name='detail'),
    path('<int:pk>/book/', views.BookAppointmentView.as_view(), name='book'),
    path('<int:pk>/reviews/', views.ProfessionalReviewsView.as_view(), name='reviews'),
    path('<int:pk>/review/add/', views.AddReviewView.as_view(), name='add_review'),
    
    # Professional dashboard (for professionals only)
    path('dashboard/', views.ProfessionalDashboardView.as_view(), name='dashboard'),
    path('dashboard/profile/', views.ProfessionalProfileEditView.as_view(), name='profile_edit'),
    path('dashboard/schedule/', views.ProfessionalScheduleView.as_view(), name='schedule'),
    path('dashboard/appointments/', views.ProfessionalAppointmentsView.as_view(), name='appointments'),
    path('dashboard/reviews/', views.ProfessionalReviewsManageView.as_view(), name='reviews_manage'),
    
    # AJAX endpoints
    path('ajax/available-slots/', views.get_available_slots, name='available_slots'),
    path('ajax/update-availability/', views.update_availability, name='update_availability'),
] 