from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from testi.models import Test

from .models import Naloga


def podrobnosti(request, id: int):
    naloga = get_object_or_404(Naloga, id=id).doloci_tip()
    _, besedilo, resitev = naloga.ustvari_primer_in_besedilo()
    return render(
        request,
        "naloge/podrobnosti.html",
        {"naloga": naloga, "besedilo": besedilo, "resitev": resitev},
    )


def izberi_tip(request, test_id: int):
    test = get_object_or_404(Test, id=test_id)
    podrazredi = Naloga.__subclasses__()
    content_types = ContentType.objects.get_for_models(*podrazredi).values()
    return render(
        request,
        "naloge/izberi_tip.html",
        {"content_types": content_types, "test": test},
    )


def dodaj(request, test_id: int, content_type_id: int):
    test = get_object_or_404(Test, id=test_id)
    content_type = ContentType.objects.get_for_id(content_type_id)
    NalogaForm = content_type.model_class().form()
    form = NalogaForm(request.POST)
    form.instance.test = test
    if form.is_valid():
        naloga: Naloga = form.save()
        return redirect("testi:podrobnosti", id=naloga.test.id)
    return render(request, "naloge/naloga_form.html", {"form": form})


def uredi(request, id: int):
    naloga = get_object_or_404(Naloga, id=id).doloci_tip()
    NalogaForm = naloga.form()
    form = NalogaForm(request.POST or None, instance=naloga)
    if form.is_valid():
        naloga: Naloga = form.save()
        return redirect("testi:podrobnosti", id=naloga.test.id)
    return render(request, "naloge/naloga_form.html", {"form": form})


def pobrisi(request, id: int):
    naloga = get_object_or_404(Naloga, id=id)
    naloga.delete()
    return redirect("testi:podrobnosti", id=naloga.test.id)
