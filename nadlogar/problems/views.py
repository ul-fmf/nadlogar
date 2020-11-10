from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from quizzes.models import Quiz

from .models import Problem


def details(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id).refine_class()
    _, question, answer = problem.generate_everything()
    return render(
        request,
        "problems/details.html",
        {"problem": problem, "question": question, "answer": answer},
    )


def choose_generator(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    subclasses = Problem.__subclasses__()
    content_types = ContentType.objects.get_for_models(*subclasses).values()
    return render(
        request,
        "problems/choose_generator.html",
        {"content_types": content_types, "quiz": quiz},
    )


def create(request, quiz_id: int, content_type_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    content_type = ContentType.objects.get_for_id(content_type_id)
    ProblemForm = content_type.model_class().form()
    form = ProblemForm(request.POST)
    form.instance.quiz = quiz
    if form.is_valid():
        problem: Problem = form.save()
        return redirect("quizzes:details", quiz_id=problem.quiz.id)
    return render(request, "problems/problem_form.html", {"form": form})


def edit(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id).refine_class()
    ProblemForm = problem.form()
    form = ProblemForm(request.POST or None, instance=problem)
    if form.is_valid():
        problem: Problem = form.save()
        return redirect("quizzes:details", quiz_id=problem.quiz.id)
    return render(request, "problems/problem_form.html", {"form": form})


def delete(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id)
    problem.delete()
    return redirect("quizzes:details", quiz_id=problem.quiz.problem_id)
