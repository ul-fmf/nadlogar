from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import problem_form
from .models import Problem, problem_content_types


def _get_problem_if_allowed(request, problem_id):
    problem = get_object_or_404(
        Problem.objects.select_related("document__student_group__user"), id=problem_id
    )
    if problem.document.student_group.user == request.user:
        return problem
    else:
        raise PermissionDenied


@login_required
def choose_problem(request, document_id):
    content_types = [
        (content_type.id, generator._meta.verbose_name)
        for generator, content_type in problem_content_types().items()
    ]
    return render(
        request,
        "problems/choose_problem.html",
        {"document_id": document_id, "content_types": content_types},
    )


@login_required
def create_problem(request):
    content_type_id = request.GET.get("content_type") or request.POST.get(
        "content_type"
    )
    content_type = get_object_or_404(ContentType, id=content_type_id)
    if request.method == "POST":
        form = problem_form(content_type, request.POST or None)
        if form.is_valid():
            problem: Problem = form.save()
            return redirect("documents:view_document", document_id=problem.document.id)
    else:
        form = problem_form(content_type, initial=request.GET.dict())
    return render(
        request,
        "problems/create_problem.html",
        {"form": form},
    )


@login_required
def edit_problem(request, problem_id: int):
    problem = _get_problem_if_allowed(request, problem_id).downcast()
    form = problem_form(problem.content_type, request.POST or None, instance=problem)
    if request.method == "POST" and form.is_valid():
        problem: Problem = form.save()
        return redirect("documents:view_document", document_id=problem.document.id)
    return render(request, "problems/edit_problem.html", {"form": form})


@login_required
def delete_problem(request, problem_id: int):
    problem = _get_problem_if_allowed(request, problem_id)
    problem.delete()
    return redirect("documents:view_document", document_id=problem.document.id)
