# Contributing

Dodajanje novih funkcionalnosti ali popravljanje napak se dogaja prek
pull requestov (PR). To najlažje naredite prek svojega forka repozitorija.
Vsebino PR in commitov pišite v slovenščini.

Poskrbite, da PR ni prevelik in da je zaključena celota. Po vsakem PR mora aplikacija še vedno
delovati. Pri vsakem PR:

* napišite smiselen naslov, ki pove, kaj PR naredi;
* napišite opis, kjer opišete, kaj je problem in kako ga rešite (lahko se sklicujete ali zaprete
  primeren issue)
* commiti v PRju so zaključene celote (če je potrebno kaj popraviti, uredite obstoječi commit in
  ne naredite novega)
* sprememba naj bo ena sama in koda naj bo čimbolj berljiva
* PR mora na githubu dobiti kljukico, da so vsi avtomatski testi ok (po #15 in #25). To vključuje
  - test stila kode
  - test generiranja dokumentacije
  - test funkcionalnosti

Te tri teste lahko poženete tudi lokalno (glejte ukaze v [.github/workflows/](.github/workflows/)).
Za poganjanje je potrebno imeti instaliran `black` in `sphinx`. Morebitne napake popravite tako, da
uredite svoje commite (ne dodati na koncu enega commita, ki popravi vse napake). Enako velja za
spremembe med procesom pregleda.

Po prvem uspešno sprejetem PRju boste tudi dodani na seznam razvijalcev.
