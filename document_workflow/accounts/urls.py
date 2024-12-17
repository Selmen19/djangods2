from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    # API routes for users
    path('api/', include(router.urls)), 

    # Authentication routes
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # User role-based dashboards
    path('manager/', views.manager_dashboard, name='manager_dashboard'),

    # Home page route
    path('home/', views.home, name='home'),  # This handles the home route

    # Other URLs as needed
]
