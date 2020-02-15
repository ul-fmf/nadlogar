from django.shortcuts import get_object_or_404, render

from .models import Test


def index(request):
    seznam_testov = Test.objects.all()
    return render(request, 'testi/index.html', {'seznam_testov': seznam_testov})


def podrobnosti(request, pk: int):
    test: Test = get_object_or_404(Test, pk=pk)
    return render(request, 'testi/podrobnosti.html', {'test': test})


def nadloga(request, pk: int):
    test: Test = get_object_or_404(Test, pk=pk)
    return render(request, 'testi/nadloga.html', {'test': test, 'nadloga': test.ustvari_nadlogo()})
