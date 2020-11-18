from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm, StudentGroupForm
from .models import Student, StudentGroup


def index(request):
    groups = StudentGroup.objects.all()
    return render(request, "students/index.html", {"groups": groups})


def create_group(request):
    form = StudentGroupForm(request.POST or None)
    if form.is_valid():
        group: StudentGroup = form.save()
        return redirect("students:details", group_id=group.id)
    return render(request, "students/group_form.html", {"form": form})


def details(request, group_id: int):
    group = get_object_or_404(StudentGroup, id=group_id)
    return render(request, "students/details.html", {"group": group})


def edit_group(request, group_id: int):
    group = get_object_or_404(StudentGroup, id=group_id)
    form = StudentGroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group: StudentGroup = form.save()
        return redirect("students:details", group_id=group.id)
    return render(request, "students/group_form.html", {"form": form})


def delete_group(request, group_id: int):
    group = get_object_or_404(StudentGroup, id=group_id)
    group.delete()
    return redirect("students:index")


def create_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student: Student = form.save()
        return redirect("students:details", group_id=student.group.id)
    return render(request, "students/student_form.html", {"form": form})


def edit_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        student: Student = form.save()
        return redirect("students:details", student_id=student.id)
    return render(request, "students/student_form.html", {"form": form})


def delete_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect("students:details", group_id=student.group.id)
