from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

# API router for CustomUser model
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    # API routes for users
    path('api/', include(router.urls)), 

    # Authentication routes
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # Role-based dashboards
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Home page
    path('home/', views.home, name='home'),


]
