from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProblemForm, problem_parameters_form, problem_text_form
from .models import Problem


def _get_problem_if_allowed(request, problem_id):
    problem = get_object_or_404(
        Problem.objects.select_related("quiz__student_group__user"), id=problem_id
    )
    if problem.quiz.student_group.user == request.user:
        return problem
    else:
        raise PermissionDenied


@login_required
def create_problem(request):
    problem_form = ProblemForm(request.POST or request.GET or None)
    if problem_form.is_valid():
        content_type = problem_form.cleaned_data["content_type"]
        return create_parameters(request, content_type)
    return render(
        request,
        "problems/create_generator.html",
        {"form": problem_form},
    )


@login_required
def create_parameters(request, content_type):
    parameters_form = problem_parameters_form(
        content_type, request.POST or request.GET or None
    )
    if parameters_form.is_valid():
        return create_text(request, parameters_form.instance)
    return render(
        request,
        "problems/create_parameters.html",
        {"form": parameters_form},
    )


@login_required
def create_text(request, problem):
    text_form = problem_text_form(
        problem, request.POST or request.GET or None, initial={"text": None}
    )
    if request.method == "POST" and text_form.is_valid():
        problem = text_form.save()
        return redirect("quizzes:view_quiz", quiz_id=problem.quiz.id)
    return render(
        request,
        "problems/create_text.html",
        {"form": text_form},
    )


@login_required
def edit_parameters(request, problem_id: int):
    problem = _get_problem_if_allowed(request, problem_id).downcast()
    form = problem_parameters_form(
        problem.content_type, request.POST or None, instance=problem
    )
    if request.method == "POST" and form.is_valid():
        problem: Problem = form.save()
        return redirect("quizzes:view_quiz", quiz_id=problem.quiz.id)
    return render(request, "problems/edit_parameters.html", {"form": form})


@login_required
def edit_text(request, problem_id: int):
    problem = _get_problem_if_allowed(request, problem_id).downcast()
    form = problem_text_form(problem, request.POST or None, instance=problem)
    if request.method == "POST" and form.is_valid():
        problem: Problem = form.save()
        return redirect("quizzes:view_quiz", quiz_id=problem.quiz.id)
    return render(request, "problems/edit_text.html", {"form": form})


@login_required
def delete_problem(request, problem_id: int):
    problem = _get_problem_if_allowed(request, problem_id)
    problem.delete()
    return redirect("quizzes:view_quiz", quiz_id=problem.quiz.id)
