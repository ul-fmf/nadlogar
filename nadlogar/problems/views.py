from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from quizzes.models import Quiz

from .forms import ProblemForm, problem_parameters_form, problem_text_form
from .models import Problem


def create(request):
    problem_form = ProblemForm(request.POST or None)
    if problem_form.is_valid():
        content_type = problem_form.cleaned_data["content_type"]
        model_class = content_type.model_class()
        return create_parameters(request, model_class)
    return render(
        request,
        "problems/choose_generator.html",
        {"form": problem_form},
    )


def create_parameters(request, model_class):
    parameters_form = problem_parameters_form(model_class, request.POST or None)
    if parameters_form.is_valid():
        return create_text(request, model_class)
    return render(
        request,
        "problems/choose_parameters.html",
        {"form": parameters_form},
    )


def create_text(request, model_class):
    text_form = problem_text_form(
        model_class, request.POST or None, initial={"text": None}
    )
    if text_form.is_valid():
        problem = text_form.save()
        return redirect("quizzes:details", quiz_id=problem.quiz.id)
    return render(
        request,
        "problems/choose_text.html",
        {"form": text_form},
    )


def details(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id).downcast()
    _, question, answer = problem.generate_everything()
    return render(
        request,
        "problems/details.html",
        {"problem": problem, "question": question, "answer": answer},
    )


def edit_parameters(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id).downcast()
    form = problem_parameters_form(
        type(problem), request.POST or None, instance=problem
    )
    if form.is_valid():
        problem: Problem = form.save()
        return redirect("quizzes:details", quiz_id=problem.quiz.id)
    return render(request, "problems/choose_parameters.html", {"form": form})


def edit_text(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id).downcast()
    form = problem_text_form(type(problem), request.POST or None, instance=problem)
    if form.is_valid():
        problem: Problem = form.save()
        return redirect("quizzes:details", quiz_id=problem.quiz.id)
    return render(request, "problems/choose_text.html", {"form": form})


def delete(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id)
    problem.delete()
    return redirect("quizzes:details", quiz_id=problem.quiz.id)
