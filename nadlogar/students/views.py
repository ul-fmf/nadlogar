from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm, StudentGroupForm
from .models import Student, StudentGroup


def create_group(request):
    form = StudentGroupForm(request.POST or None)
    if form.is_valid():
        group: StudentGroup = form.save()
        return redirect("students:view_group", group_id=group.id)
    return render(request, "students/group_form.html", {"form": form})


def view_group(request, group_id: int):
    group = get_object_or_404(StudentGroup, id=group_id)
    return render(request, "students/view_group.html", {"group": group})


def edit_group(request, group_id: int):
    group = get_object_or_404(StudentGroup, id=group_id)
    form = StudentGroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group: StudentGroup = form.save()
        return redirect("students:view_group", group_id=group.id)
    return render(request, "students/edit_group.html", {"form": form})


def delete_group(request, group_id: int):
    group = get_object_or_404(StudentGroup, id=group_id)
    group.delete()
    return redirect("homepage")


def create_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student: Student = form.save()
        return redirect("students:view_group", group_id=student.group.id)
    return render(request, "students/create_student.html", {"form": form})


def edit_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        student: Student = form.save()
        return redirect("students:view_group", group_id=student.group.id)
    return render(request, "students/edit_student.html", {"form": form})


def delete_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect("students:view_group", group_id=student.group.id)
