from .models import StudentGroup


def my_groups(request):
    if request.user.is_authenticated:
        return {
            "my_groups": StudentGroup.objects.filter(user=request.user),
        }
    else:
        return {}
