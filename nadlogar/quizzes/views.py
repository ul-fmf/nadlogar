from django.shortcuts import get_object_or_404, redirect, render

from .forms import QuizForm
from .models import Quiz


def create_quiz(request):
    form = QuizForm(request.POST or request.GET or None)
    if form.is_valid():
        quiz: Quiz = form.save()
        return redirect("quizzes:view_quiz", quiz_id=quiz.id)
    return render(request, "quizzes/create_quiz.html", {"form": form})


def view_quiz(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(
        request,
        "quizzes/view_quiz.html",
        {"quiz": quiz},
    )


def edit_quiz(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuizForm(request.POST or None, instance=quiz)
    if form.is_valid():
        quiz: Quiz = form.save()
        return redirect("quizzes:view_quiz", quiz_id=quiz.id)
    return render(request, "quizzes/edit_quiz.html", {"form": form})


def delete_quiz(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect("homepage")


def generate(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(
        request,
        "quizzes/generate.html",
        {"quiz": quiz, "generated_problems": quiz.generate_everything()},
    )
