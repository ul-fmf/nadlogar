from .models import Quiz


def my_quizzes(request):
    if request.user.is_authenticated:
        return {
            "my_quizzes": Quiz.objects.filter(student_group__user=request.user),
        }
    else:
        return {}
