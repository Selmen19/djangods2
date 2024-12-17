from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class AccountTests(TestCase):
    def setUp(self):
        # Set up a test custom user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_user_creation(self):
        """Test that the user is created with the correct username and password."""
        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))  # Check if the password matches

    def test_user_login_view(self):
        """Test the login page for the user."""
        response = self.client.get(reverse('login'))  # Adjust to your login URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')  # Ensure the login page template is used

        # Login with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('home'))  # Adjust to the URL to redirect after login

    def test_user_logout_view(self):
        """Test the logout view."""
        self.client.login(username='testuser', password='testpassword')  # Log the user in first
        response = self.client.get(reverse('logout'))  # Adjust to your logout URL name
        self.assertRedirects(response, reverse('home'))  # After logout, it should redirect to the home page

    def test_login_required_view(self):
        """Test that a view requires login."""
        response = self.client.get(reverse('profile'))  # A view that requires login (adjust as needed)
        self.assertRedirects(response, '/accounts/login/?next=/profile/')  # Ensure it redirects to login page

    def test_custom_user_model_fields(self):
        """Test custom fields on the custom user model."""
        # For example, if you added a 'bio' field to the CustomUser model
        user = get_user_model().objects.create_user(
            username='testuser2',
            password='testpassword',
            email='testuser2@example.com',
            bio='This is a test bio.'
        )
        self.assertEqual(user.bio, 'This is a test bio.')  # Check if custom field is correctly saved

    def test_user_permission(self):
        """Test that user permissions are assigned correctly."""
        permission = Permission.objects.get(codename='add_document')  # Adjust to an existing permission
        self.user.user_permissions.add(permission)
        self.assertTrue(self.user.has_perm('documents.add_document'))  # Test if the permission is assigned properly

