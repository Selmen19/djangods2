from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm
from .models import CustomUser
from rest_framework import viewsets
from accounts.serializers import CustomUserSerializer


# Register view for new users
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully registered!")
            return redirect('login')
        else:
            # Print form errors to the console for debugging
            print(form.errors)
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})



# Login view for authenticating users
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Validate credentials
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'accounts/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect_based_on_role(user)  # Redirect based on the user's role
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'accounts/login.html')


# Protected view for the manager dashboard (requires login and specific permission)
@login_required
@permission_required('accounts.can_approve_documents', raise_exception=True)  # Adjusted permission name
def manager_dashboard(request):
    return render(request, 'dashboard/manager.html')


# A fallback for users without permission, or unauthenticated access
def permission_denied(request):
    return HttpResponseForbidden('You do not have permission to view this page.')


# Home page after successful login or registration
@login_required
def home(request):
    return render(request, 'accounts/home.html')  # Ensure this points to the correct template path


# Redirect user based on their role (this can be called after login)
def redirect_based_on_role(user):
    if hasattr(user, 'role'):  # Ensure 'role' exists in your user model
        if user.role == 'admin':
            return redirect('admin_dashboard')  # Replace with your actual admin dashboard URL name
        elif user.role == 'manager':
            return redirect('manager_dashboard')  # Replace with your actual manager dashboard URL name
        elif user.role == 'employee':
            return redirect('employee_dashboard')  # Replace with your actual employee dashboard URL name
    return redirect('home')  # Default redirection if the role is not recognized


# View for handling CustomUser API requests
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# Views for different dashboards
@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')  # Ensure this points to the correct template path

@login_required
def employee_dashboard(request):
    return render(request, 'dashboard/employee.html')  # Ensure this points to the correct template path
