from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from documents.models import Document


@login_required
def homepage(request):
    documents = Document.objects.filter(student_group__user=request.user)
    return render(request, "homepage.html", {"documents": documents})
