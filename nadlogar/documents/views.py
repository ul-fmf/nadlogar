from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentForm
from .models import Document


def _get_document_if_allowed(request, document_id):
    document = get_object_or_404(
        Document.objects.select_related("student_group__user"), id=document_id
    )
    if document.student_group.user == request.user:
        return document
    else:
        raise PermissionDenied


@login_required
def create_document(request):
    form = DocumentForm(request.user, request.POST or request.GET or None)
    if form.is_valid():
        document: Document = form.save(commit=False)
        if document.student_group.user == request.user:
            document.save()
            return redirect("documents:view_document", document_id=document.id)
        else:
            raise PermissionDenied
    return render(request, "documents/create_document.html", {"form": form})


@login_required
def view_document(request, document_id: int):
    document = _get_document_if_allowed(request, document_id)
    return render(
        request,
        "documents/view_document.html",
        {"document": document},
    )


@login_required
def edit_document(request, document_id: int):
    document = _get_document_if_allowed(request, document_id)
    form = DocumentForm(request.user, request.POST or None, instance=document)
    if form.is_valid():
        document: Document = form.save()
        return redirect("documents:view_document", document_id=document.id)
    return render(request, "documents/edit_document.html", {"form": form})


@login_required
def delete_document(request, document_id: int):
    document = _get_document_if_allowed(request, document_id)
    document.delete()
    return redirect("homepage")


@login_required
def generate(request, document_id: int):
    document = _get_document_if_allowed(request, document_id)
    return render(
        request,
        "documents/generate.html",
        {"document": document, "generated_problems": document.generate_data_and_text()},
    )
