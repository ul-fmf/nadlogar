from django.shortcuts import get_object_or_404, render

from .models import Naloga


def index(request):
    seznam_nalog = Naloga.objects.all()
    return render(request, 'naloge/index.html', {'seznam_nalog': seznam_nalog})


def podrobnosti(request, pk: int):
    naloga: Naloga = get_object_or_404(Naloga, pk=pk)
    return render(request, 'naloge/podrobnosti.html', {'naloga': naloga})


def primer(request, pk: int):
    naloga: Naloga = get_object_or_404(Naloga, pk=pk)
    return render(request, naloga.ime_predloge(), {'primer': naloga.ustvari_primer()})
