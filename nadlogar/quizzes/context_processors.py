from .models import Quiz


def my_quizzes(request):
    return {
        "my_quizzes": Quiz.objects.all(),
        "quiz": None,
    }
