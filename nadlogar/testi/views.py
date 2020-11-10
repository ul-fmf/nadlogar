from django.shortcuts import get_object_or_404, redirect, render

from .models import Test
from .forms import TestForm


def seznam(request):
    testi = Test.objects.all()
    return render(request, "testi/seznam.html", {"testi": testi})


def podrobnosti(request, id: int):
    test = get_object_or_404(Test, id=id)
    return render(request, "testi/podrobnosti.html", {"test": test})


def nadloga(request, id: int):
    test = get_object_or_404(Test, id=id)
    return render(
        request, "testi/nadloga.html", {"test": test, "nadloga": test.ustvari_nadlogo()}
    )


def dodaj(request):
    form = TestForm(request.POST)
    if form.is_valid():
        test: Test = form.save()
        return redirect("testi:podrobnosti", id=test.id)
    return render(request, "testi/test_form.html", {"form": form})


def uredi(request, id: int):
    test = get_object_or_404(Test, id=id)
    form = TestForm(request.POST or None, instance=test)
    if form.is_valid():
        test: Test = form.save()
        return redirect("testi:podrobnosti", id=test.id)
    return render(request, "testi/test_form.html", {"form": form})


def pobrisi(request, id: int):
    test = get_object_or_404(Test, id=id)
    test.delete()
    return redirect("testi:seznam")
