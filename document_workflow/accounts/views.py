# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from rest_framework import viewsets
from .forms import CustomUserCreationForm, DocumentForm
from .models import CustomUser, Document
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
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'accounts/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect user based on their role
            return redirect_based_on_role(user)
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'accounts/login.html')

# Redirect user based on their role
def redirect_based_on_role(user):
    # Check for user role, assuming role is a custom field or group-based permissions
    if hasattr(user, 'role'):
        if user.role == 'admin':
            return redirect('admin_dashboard')
        elif user.role == 'manager':
            return redirect('manager_dashboard')
        elif user.role == 'employee':
            return redirect('employee_dashboard')
    return redirect('home')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

@login_required
@permission_required('accounts.can_approve_documents', raise_exception=True)
def manager_dashboard(request):
    return render(request, 'dashboard/manager.html')

@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')

@login_required
def employee_dashboard(request):
    return render(request, 'dashboard/employee.html')

# Document CRUD Views
@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # Ensure file handling is included
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user  # Set the current user as the uploader
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_form.html', {'form': form})

@login_required
def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully!')
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/document_form.html', {'form': form})

@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    messages.success(request, 'Document deleted successfully!')
    return redirect('document_list')

@login_required
@permission_required('documents.can_approve_documents', raise_exception=True)
def document_approve(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.status = 'Approved'
    document.save()
    messages.success(request, 'Document approved successfully!')
    return redirect('document_list')

@login_required
@permission_required('documents.can_approve_documents', raise_exception=True)
def document_reject(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.status = 'Rejected'
    document.save()
    messages.success(request, 'Document rejected.')
    return redirect('document_list')

# API View for CustomUser
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
