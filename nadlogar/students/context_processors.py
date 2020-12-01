from .models import StudentGroup


def my_groups(request):
    return {
        "my_groups": StudentGroup.objects.all(),
        "group": None,
    }
