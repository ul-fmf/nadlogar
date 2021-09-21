from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from documents.models import Document
from students.models import StudentGroup


@login_required
def homepage(request):
    documents = Document.objects.filter(student_group__user=request.user)[:3]
    groups = StudentGroup.objects.filter(user=request.user)
    return render(request, "homepage.html", {"documents": documents, "groups": groups})
