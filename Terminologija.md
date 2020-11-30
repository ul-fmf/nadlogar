## Generator

Program, ki v odvisnosti od parametrov sestavi podatke problema, npr. `poisci_nicle_polinoma(stopnja_polinoma, max_koeficient)`

## Podatki problema

Tisto, kar za dane parametre vrne generator, npr. `{'polinom': 'x^3 - x', 'nicle': [-1, 0, 1]}`.

## Besedilo problema

Vzorec, v katerega vstavimo podatke problema, npr. `"Poiščite vse ničle polinoma ${{polinom}}$$."`.

## Problem

Generator (npr. `poisci_nicle_polinoma`) skupaj s konkretnimi parametri, npr. `stopnja_polinoma = 3`, `max_koeficent = 9`, ter besedilom.

## Kviz

Seznam problemov in morebitni dodatni parametri (datum, seznam učencev, predloga kviza, …)

## Nadloga

Nekaj, kar zgeneriramo iz kviza, torej konkretni problemi za konkretne učence.
