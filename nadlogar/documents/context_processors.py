from .models import Document


def my_documents(request):
    if request.user.is_authenticated:
        return {
            "my_documents": Document.objects.filter(student_group__user=request.user),
        }
    else:
        return {}
