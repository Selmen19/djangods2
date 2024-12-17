from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.contrib.contenttypes.models import ContentType

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return f"{self.username} ({self.role})"

    @staticmethod
    def create_permissions():
        # List of permissions to create
        permissions = [
            {'codename': 'can_approve_documents', 'name': 'Can Approve Documents'},
            {'codename': 'can_view_reports', 'name': 'Can View Reports'},
            {'codename': 'can_upload_documents', 'name': 'Can Upload Documents'},
        ]
        
        # Get the content type for the CustomUser model
        content_type = ContentType.objects.get_for_model(CustomUser)

        # Create permissions if they don't exist
        for perm in permissions:
            permission, created = Permission.objects.get_or_create(
                codename=perm['codename'], 
                name=perm['name'],
                content_type=content_type
            )
            if created:
                print(f"Created permission: {perm['name']}")
            else:
                print(f"Permission already exists: {perm['name']}")

class Document(models.Model):
    user = models.ForeignKey(CustomUser, related_name='documents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


