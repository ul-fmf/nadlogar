from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from documents.views import _get_document_if_allowed

from .forms import problem_form
from .models import Problem, problem_content_types


def _get_problem_if_allowed(request, group_id: int, document_id: int, problem_id):
    problem = get_object_or_404(
        Problem.objects.select_related("document__student_group__user"),
        document__student_group__id=group_id,
        document__id=document_id,
        id=problem_id,
    )
    if problem.document.student_group.user == request.user:
        return problem
    else:
        raise PermissionDenied


@login_required
def choose_problem(request, group_id: int, document_id: int):
    problem_groups = {}
    for generator, content_type in problem_content_types().items():
        group, description = generator._meta.verbose_name.split(" / ")
        problem_groups.setdefault(group, []).append(
            (
                content_type.id,
                content_type.model_class().example_data_and_text()[1],
                description,
            )
        )
    if "???" in problem_groups:
        del problem_groups["???"]
    special_problems = problem_groups.pop("Razno")
    grouped_problems = [("Razno", special_problems)] + sorted(problem_groups.items())
    document = _get_document_if_allowed(request, group_id, document_id)
    return render(
        request,
        "problems/choose_problem.html",
        {"document": document, "grouped_problems": grouped_problems},
    )


@login_required
def create_problem(request, group_id: int, document_id: int, content_type_id: int):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    document = _get_document_if_allowed(request, group_id, document_id)
    example_data, example_text = content_type.model_class().example_data_and_text()
    form = problem_form(content_type, request.POST or None)
    if form.is_valid():
        problem: Problem = form.save(commit=False)
        problem.document = document
        problem.save()
        return redirect(problem.document.get_absolute_url())
    return render(
        request,
        "problems/create_problem.html",
        {
            "document": document,
            "form": form,
            "example_data": example_data,
            "example_text": example_text,
        },
    )


@login_required
def edit_problem(request, group_id: int, document_id: int, problem_id: int):
    problem = _get_problem_if_allowed(
        request, group_id, document_id, problem_id
    ).downcast()
    form = problem_form(problem.content_type, request.POST or None, instance=problem)
    if form.is_valid():
        problem: Problem = form.save()
        return redirect(problem.document.get_absolute_url())
    example_data = problem.generate_data_and_text()[0]
    example_text = problem.default_text().render(example_data)
    return render(
        request,
        "problems/edit_problem.html",
        {
            "problem": problem,
            "form": form,
            "example_data": example_data,
            "example_text": example_text,
        },
    )


@login_required
def delete_problem(request, group_id: int, document_id: int, problem_id: int):
    problem = _get_problem_if_allowed(request, group_id, document_id, problem_id)
    if request.method == "POST":
        problem.delete()
        return redirect(problem.document.get_absolute_url())
    return render(request, "problems/delete_problem.html", {"problem": problem})


@login_required
def duplicate_problem(request, group_id: int, document_id: int, problem_id: int):
    problem = _get_problem_if_allowed(request, group_id, document_id, problem_id)
    if request.method == "POST":
        new_problem = problem.copy(problem.document)
        return redirect(new_problem.document.get_absolute_url())
