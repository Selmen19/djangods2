from django.db import migrations


def create_permissions(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')  # Ensure this points to the correct app and model
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
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
        Permission.objects.get_or_create(
            codename=perm['codename'],
            name=perm['name'],
            content_type=content_type
        )


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),  # Adjust to match the previous migration file
    ]

    operations = [
        migrations.RunPython(create_permissions),
    ]
