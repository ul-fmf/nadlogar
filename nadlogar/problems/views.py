from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from documents.views import _get_document_if_allowed

from .forms import problem_form
from .models import Problem, problem_content_types


def _get_problem_if_allowed(request, group_id: int, document_id: int, problem_id):
    """Returns the problem if the user is allowed to edit it.

    Raises PermissionDenied if the user is not allowed to edit the problem."""
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
    """Displays a page where the user can choose a problem type."""
    problem_groups = {}
    for generator, content_type in problem_content_types().items():
        group, description = generator._meta.verbose_name.split(" / ")
        # We create an instance of the generator class to get the example text.
        Generator = content_type.model_class()
        example_problem = Generator()
        example_text = example_problem.example_text()
        problem_groups.setdefault(group, []).append(
            (
                content_type.id,
                example_text,
                description,
            )
        )
    # We use the "???" group as a hack for any problems we do not want to display.
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
    """Displays a page where the user can create a problem."""
    content_type = get_object_or_404(ContentType, id=content_type_id)
    document = _get_document_if_allowed(request, group_id, document_id)
    # We create an instance of the generator class to get the example text.
    Generator = content_type.model_class()
    example_problem = Generator()
    example_data = example_problem.example_data()
    default_text = example_problem.render(example_data, default_text=True)
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
            "example_datum": example_data[0],
            "default_text": default_text,
        },
    )


@login_required
def edit_problem(request, group_id: int, document_id: int, problem_id: int):
    """Displays a page where the user can edit a problem."""
    problem = _get_problem_if_allowed(
        request, group_id, document_id, problem_id
    ).downcast()
    form = problem_form(problem.content_type, request.POST or None, instance=problem)
    if form.is_valid():
        problem: Problem = form.save()
        return redirect(problem.document.get_absolute_url())
    # We display the example data as a dictionary of values that the user can
    # use in templates.
    example_data = problem.example_data()
    # We also render the problem with default text if the user wants to switch
    # back to the default text.
    default_text = problem.render(example_data, default_text=True)
    return render(
        request,
        "problems/edit_problem.html",
        {
            "problem": problem,
            "form": form,
            "example_datum": example_data[0],
            "default_text": default_text,
        },
    )


@login_required
def delete_problem(request, group_id: int, document_id: int, problem_id: int):
    """Displays a page where the user can delete a problem.

    If the user confirms the deletion, the problem is deleted and the user is
    redirected to the document page."""
    problem = _get_problem_if_allowed(request, group_id, document_id, problem_id)
    if request.method == "POST":
        problem.delete()
        return redirect(problem.document.get_absolute_url())
    return render(request, "problems/delete_problem.html", {"problem": problem})


@login_required
def duplicate_problem(request, group_id: int, document_id: int, problem_id: int):
    """Duplicates a problem and redirects to the document page."""
    problem = _get_problem_if_allowed(request, group_id, document_id, problem_id)
    if request.method == "POST":
        new_problem = problem.copy(problem.document)
        return redirect(new_problem.document.get_absolute_url())
