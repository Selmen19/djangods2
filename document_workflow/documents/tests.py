from django.test import TestCase
from django.urls import reverse
from .models import Document
from accounts.models import CustomUser  # Import the custom user model


class DocumentTests(TestCase):
    def setUp(self):
        # Set up a test custom user and a test document
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')  # Use CustomUser
        self.document = Document.objects.create(title='Test Document', file='testfile.pdf')

    def test_document_list_view(self):
        response = self.client.get(reverse('document_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')  # Check if the document is listed
        self.assertTemplateUsed(response, 'documents/document_list.html')  # Ensure correct template is used

    def test_document_create_view(self):
        self.client.login(username='testuser', password='testpassword')  # Log in if needed
        response = self.client.get(reverse('document_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_create.html')

    def test_document_detail_view(self):
        response = self.client.get(reverse('document_detail', args=[self.document.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')  # Ensure the document title is shown

    def test_document_edit_view(self):
        response = self.client.get(reverse('document_edit', args=[self.document.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_edit.html')

    def test_document_delete_view(self):
        response = self.client.get(reverse('document_delete', args=[self.document.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_confirm_delete.html')

    def test_document_delete_post(self):
        response = self.client.post(reverse('document_delete', args=[self.document.pk]))
        self.assertRedirects(response, reverse('document_list'))  # After delete, it should redirect to the list view
        self.assertFalse(Document.objects.filter(pk=self.document.pk).exists())  # Check if document is deleted
