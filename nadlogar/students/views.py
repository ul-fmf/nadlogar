from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm, StudentGroupForm
from .models import Student, StudentGroup


def get_group_if_allowed(request, group_id):
    group = get_object_or_404(StudentGroup.objects.select_related("user"), id=group_id)
    if group.user == request.user:
        return group
    else:
        raise PermissionDenied


def _get_student_if_allowed(request, group_id, student_id):
    student = get_object_or_404(
        Student.objects.select_related("group__user"),
        id=student_id,
        group__id=group_id,
    )
    if student.group.user == request.user:
        return student
    else:
        raise PermissionDenied


@login_required
def create_group(request):
    form = StudentGroupForm(request.POST or None)
    if form.is_valid():
        group: StudentGroup = form.save(commit=False)
        group.user = request.user
        group.save()
        return redirect(group.get_absolute_url())
    return render(request, "students/create_group.html", {"form": form})


@login_required
def view_group(request, group_id: int):
    group = get_group_if_allowed(request, group_id)
    return render(request, "students/view_group.html", {"group": group})


@login_required
def view_students(request, group_id: int):
    group = get_group_if_allowed(request, group_id)
    return render(request, "students/view_students.html", {"group": group})


@login_required
def edit_group(request, group_id: int):
    group = get_group_if_allowed(request, group_id)
    form = StudentGroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group: StudentGroup = form.save()
        return redirect(group.get_absolute_url())
    return render(request, "students/edit_group.html", {"group": group, "form": form})


@login_required
def delete_group(request, group_id: int):
    group = get_group_if_allowed(request, group_id)
    if request.method == "POST":
        group.delete()
        return redirect("homepage")
    return render(request, "students/delete_group.html", {"group": group})


@login_required
def create_student(request, group_id: int):
    group = get_group_if_allowed(request, group_id)
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student: Student = form.save(commit=False)
        student.group = group
        student.save()
        return redirect(student.group.get_absolute_url())
    return render(
        request, "students/create_student.html", {"group": group, "form": form}
    )


@login_required
def edit_student(request, group_id: int, student_id: int):
    student = _get_student_if_allowed(request, group_id, student_id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        student: Student = form.save()
        return redirect(student.group.get_absolute_url())
    return render(request, "students/edit_student.html", {"group": group, "form": form})


@login_required
def delete_student(request, group_id: int, student_id: int):
    student = _get_student_if_allowed(request, group_id, student_id)
    if request.method == "POST":
        student.delete()
        return redirect(student.group.get_absolute_url())
    return render(request, "students/delete_student.html", {"student": student})
