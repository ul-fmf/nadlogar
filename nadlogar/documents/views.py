from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from students.views import get_group_if_allowed

from .forms import DocumentForm
from .models import Document


def _get_document_if_allowed(request, group_id, document_id):
    document = get_object_or_404(
        Document.objects.select_related("student_group__user"),
        id=document_id,
        student_group__id=group_id,
    )
    if document.student_group.user == request.user:
        return document
    else:
        raise PermissionDenied


@login_required
def create_document(request, group_id):
    group = get_group_if_allowed(request, group_id)
    form = DocumentForm(request.POST or None)
    if form.is_valid():
        document: Document = form.save(commit=False)
        document.student_group = group
        document.save()
        return redirect(
            "students:documents:view_document",
            group_id=document.student_group.id,
            document_id=document.id,
        )
    return render(
        request,
        "documents/create_document.html",
        {"form": form, "student_group": group},
    )


@login_required
def view_document(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    return render(
        request,
        "documents/view_document.html",
        {"document": document},
    )


@login_required
def edit_document(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    form = DocumentForm(request.POST or None, instance=document)
    if form.is_valid():
        document: Document = form.save()
        return redirect(
            "students:documents:view_document",
            group_id=document.student_group.id,
            document_id=document.id,
        )
    return render(
        request, "documents/edit_document.html", {"document": document, "form": form}
    )


@login_required
def delete_document(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    document.delete()
    return redirect("homepage")


@login_required
def generate(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    return render(
        request,
        "documents/generate.html",
        {"document": document, "generated_files": document.generate_files()},
    )
