from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser  # Correct app name

# Register view for new users
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Assign the user to the appropriate group based on their role
            role = form.cleaned_data['role']
            if role == 'admin':
                group = Group.objects.get(name='admin')
            elif role == 'manager':
                group = Group.objects.get(name='manager')
            else:
                group = Group.objects.get(name='employee')
            user.groups.add(group)

            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

# Login view for authenticating users
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'accounts/login.html')

# Protected view for the manager dashboard (requires login and specific permission)
@login_required
@permission_required('accounts.can_approve_documents', raise_exception=True)  # Changed 'users' to 'accounts'
def manager_dashboard(request):
    return render(request, 'dashboard/manager.html')

def redirect_based_on_role(user):
    if user.role == 'admin':
        return redirect('/admin-dashboard/')
    elif user.role == 'manager':
        return redirect('/manager-dashboard/')
    elif user.role == 'employee':
        return redirect('/employee-dashboard/')
    return redirect('/')
