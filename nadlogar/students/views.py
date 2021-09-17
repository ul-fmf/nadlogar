from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm, StudentGroupForm
from .models import Student, StudentGroup


def _get_group_if_allowed(request, group_id):
    group = get_object_or_404(StudentGroup.objects.select_related("user"), id=group_id)
    if group.user == request.user:
        return group
    else:
        raise PermissionDenied


@login_required
def create_group(request):
    form = StudentGroupForm(request.POST or None)
    if form.is_valid():
        group: StudentGroup = form.save(commit=False)
        group.user = request.user
        group.save()
        return redirect("students:view_group", group_id=group.id)
    return render(request, "students/create_group.html", {"form": form})


@login_required
def view_group(request, group_id: int):
    group = _get_group_if_allowed(request, group_id)
    return render(request, "students/view_group.html", {"group": group})


@login_required
def edit_group(request, group_id: int):
    group = _get_group_if_allowed(request, group_id)
    form = StudentGroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group: StudentGroup = form.save()
        return redirect("students:view_group", group_id=group.id)
    return render(request, "students/edit_group.html", {"form": form})


@login_required
def delete_group(request, group_id: int):
    group = _get_group_if_allowed(request, group_id)
    group.delete()
    return redirect("homepage")


def _get_student_if_allowed(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related("group__user"), id=student_id
    )
    if student.group.user == request.user:
        return student
    else:
        raise PermissionDenied


@login_required
def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.user, request.POST or None)
        if form.is_valid():
            student: Student = form.save()
            if student.group.user == request.user:
                student.save()
                return redirect("students:view_group", group_id=student.group.id)
            else:
                raise PermissionDenied
    else:
        form = StudentForm(request.user, initial=request.GET.dict())
    return render(request, "students/create_student.html", {"form": form})


@login_required
def edit_student(request, student_id: int):
    student = _get_student_if_allowed(request, student_id)
    form = StudentForm(request.user, request.POST or None, instance=student)
    if form.is_valid():
        student: Student = form.save()
        return redirect("students:view_group", group_id=student.group.id)
    return render(request, "students/edit_student.html", {"form": form})


@login_required
def delete_student(request, student_id: int):
    student = _get_student_if_allowed(request, student_id)
    student.delete()
    return redirect("students:view_group", group_id=student.group.id)
