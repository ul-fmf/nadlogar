import io
import zipfile

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from students.views import get_group_if_allowed

from .forms import DocumentForm
from .models import Document, LaTeXError


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
        return redirect(document.get_absolute_url())

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
        return redirect(document.get_absolute_url())
    return render(
        request, "documents/edit_document.html", {"document": document, "form": form}
    )


@login_required
def delete_document(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    if request.method == "POST":
        document.delete()
        return redirect(document.group.get_absolute_url())
    return render(request, "documents/delete_document.html", {"document": document})


def _zip_archive(archive_name, files):
    string_buffer = io.BytesIO()
    archive = zipfile.ZipFile(string_buffer, "w", zipfile.ZIP_DEFLATED)
    for file_name, file_contents in files:
        archive.writestr(file_name, file_contents)
    archive.close()
    response = HttpResponse(string_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="{0}.zip"'.format(
        archive_name
    )
    return response


@login_required
def preview(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    return render(
        request,
        "documents/preview_download.html",
        {"document": document},
    )


@login_required
def download_tex(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    return _zip_archive(document.name, document.tex_files())


@login_required
def download_pdf(request, group_id: int, document_id: int):
    document = _get_document_if_allowed(request, group_id, document_id)
    try:
        return _zip_archive(document.name, document.pdf_files())
    except LaTeXError as error:
        return render(
            request,
            "documents/latex_error.html",
            {"document": document, "error": error},
        )
