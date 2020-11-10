from django.shortcuts import get_object_or_404, redirect, render

from .forms import QuizForm
from .models import Quiz


def index(request):
    quizzes = Quiz.objects.all()
    return render(request, "quizzes/index.html", {"quizzes": quizzes})


def details(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, "quizzes/details.html", {"quiz": quiz})


def generate(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(
        request,
        "quizzes/generate.html",
        {"quiz": quiz, "generate": quiz.generate_everything()},
    )


def create(request):
    form = QuizForm(request.POST)
    if form.is_valid():
        quiz: Quiz = form.save()
        return redirect("quizzes:details", quiz_id=quiz.id)
    return render(request, "quizzes/quiz_form.html", {"form": form})


def edit(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuizForm(request.POST or None, instance=quiz)
    if form.is_valid():
        quiz: Quiz = form.save()
        return redirect("quizzes:details", quiz_id=quiz.id)
    return render(request, "quizzes/quiz_form.html", {"form": form})


def delete(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect("quizzes:index")
