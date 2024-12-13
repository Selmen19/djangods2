from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_role_based_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'admin':
            instance.is_staff = True
            instance.is_superuser = True
        elif instance.role == 'manager':
            instance.user_permissions.add(Permission.objects.get(codename='can_approve_documents'))
        elif instance.role == 'employee':
            instance.user_permissions.add(Permission.objects.get(codename='can_upload_documents'))
        instance.save()
