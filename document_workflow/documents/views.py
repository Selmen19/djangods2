from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm  # Ensure you have a form for creating and editing documents

# View to list all documents
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/index.html', {'documents': documents})

# View to display a single document's details
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)  # Safely get the document or return a 404 if not found
    return render(request, 'documents/document_detail.html', {'document': document})

# View to create a new document
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')  # Redirect to the document list after creation
    else:
        form = DocumentForm()
    return render(request, 'documents/document_create.html', {'form': form})

# View to edit an existing document
def document_edit(request, pk):
    # Get the document to be edited, or return a 404 if not found
    document = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')  # Redirect to document list after editing
    else:
        form = DocumentForm(instance=document)

    return render(request, 'documents/document_edit.html', {'form': form, 'document': document})

def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        return redirect('document_list')  # Redirect to document list after deletion
    return render(request, 'documents/document_confirm_delete.html', {'document': document})
