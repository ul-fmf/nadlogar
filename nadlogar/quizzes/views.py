from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import QuizForm
from .models import Quiz


def _get_quiz_if_allowed(request, quiz_id):
    quiz = get_object_or_404(
        Quiz.objects.select_related("student_group__user"), id=quiz_id
    )
    if quiz.student_group.user == request.user:
        return quiz
    else:
        raise PermissionDenied


@login_required
def create_quiz(request):
    form = QuizForm(request.user, request.POST or request.GET or None)
    if form.is_valid():
        quiz: Quiz = form.save(commit=False)
        if quiz.student_group.user == request.user:
            quiz.save()
            return redirect("quizzes:view_quiz", quiz_id=quiz.id)
        else:
            raise PermissionDenied
    return render(request, "quizzes/create_quiz.html", {"form": form})


@login_required
def view_quiz(request, quiz_id: int):
    quiz = _get_quiz_if_allowed(request, quiz_id)
    return render(
        request,
        "quizzes/view_quiz.html",
        {"quiz": quiz},
    )


@login_required
def edit_quiz(request, quiz_id: int):
    quiz = _get_quiz_if_allowed(request, quiz_id)
    form = QuizForm(request.user, request.POST or None, instance=quiz)
    if form.is_valid():
        quiz: Quiz = form.save()
        return redirect("quizzes:view_quiz", quiz_id=quiz.id)
    return render(request, "quizzes/edit_quiz.html", {"form": form})


@login_required
def delete_quiz(request, quiz_id: int):
    quiz = _get_quiz_if_allowed(request, quiz_id)
    quiz.delete()
    return redirect("homepage")


@login_required
def generate(request, quiz_id: int):
    quiz = _get_quiz_if_allowed(request, quiz_id)
    return render(
        request,
        "quizzes/generate.html",
        {"quiz": quiz, "generated_problems": quiz.generate_everything()},
    )
