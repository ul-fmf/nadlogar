from django.shortcuts import get_object_or_404, redirect, render

from naloge.forms import NalogaForm

from .models import Naloga
from testi.models import Test


def podrobnosti(request, id: int):
    naloga = get_object_or_404(Naloga, id=id)
    return render(request, 'naloge/podrobnosti.html', {'naloga': naloga})


def primer(request, id: int):
    naloga = get_object_or_404(Naloga, id=id)
    return render(request, naloga.ime_predloge(), {'primer': naloga.ustvari_primer()})


def dodaj(request, test_id: int):
    test = get_object_or_404(Test, id=test_id)
    form = NalogaForm(request.POST)
    form.instance.test = test
    if form.is_valid():
        naloga: Naloga = form.save()
        return redirect('testi:podrobnosti', id=naloga.test.id)
    return render(request, 'naloge/naloga_form.html', {'form': form})


def uredi(request, id: int):
    naloga = get_object_or_404(Naloga, id=id)
    form = NalogaForm(request.POST or None, instance=naloga)
    if form.is_valid():
        naloga: Naloga = form.save()
        return redirect('testi:podrobnosti', id=naloga.test.id)
    return render(request, 'naloge/naloga_form.html', {'form': form})


def pobrisi(request, id: int):
    naloga = get_object_or_404(Naloga, id=id)
    naloga.delete()
    return redirect('testi:podrobnosti', id=naloga.test.id)
