# OSNOVNA NAVODILA ZA RAZVIJALCE NADLOGARJA

Tukaj se nahajajo osnovna navodila za uporabo Nadlogarja. Če želite pri projektu sodelovati ali kakorkoli pomagati, vam toplo priporočamo, da si jih preberete.

## Namestitev Nadlogarja

Za namestitev Nadlogarja je potrebno upoštevati navodila, ki jih najdemo na [githubu](https://github.com/ul-fmf/nadlogar).

## Dodajanje novih funkcionalnosti s pull requesti

Dodajanje novih funkcionalnosti ali popravljanje napak se dogaja prek
pull requestov (PR). To najlažje naredite prek svojega forka repozitorija.
Vsebino PR in commitov pišite v slovenščini.

Poskrbite, da PR ni prevelik in da je zaključena celota. Po vsakem PR mora aplikacija še vedno
delovati. Pri vsakem PR:

- izberite opisen naslov
- opišite problem in kako ste ga rešili (lahko se sklicujete na ali zaprete
  primeren issue)
- commiti v PRju naj bodo zaključene celote (če je potrebno kaj popraviti, uredite obstoječi commit in
  ne naredite novega)
- sprememba naj bo ena sama in koda naj bo čimbolj berljiva
- PR mora na githubu dobiti kljukico, da so vsi avtomatski testi ok. To vključuje
  - test funkcionalnosti
  - test stila kode
  - test generiranja dokumentacije (po #25)

Te tri teste lahko poženete tudi lokalno (glejte ukaze v [.github/workflows/](.github/workflows/)).
Za poganjanje je potrebno imeti instaliran `black` in `sphinx`. Kodo lahko samodejno oblikujete v
urejevalniku, lahko pa tudi poženete

    python -m black .

Morebitne napake popravite tako, da uredite svoje commite (ne dodati na koncu enega commita, ki
popravi vse napake). Enako velja za spremembe med procesom pregleda.

Po prvem uspešno sprejetem PRju boste tudi dodani na seznam razvijalcev.

## Dodajanje nove naloge

Za dodajanje novega problema je potrebno:

- V datoteko `nadlogar/problems/<ime_datoteke>.py` dodati nov podrazred razreda `Problem`.
- V dokumentacijski niz razreda napisati en stavek, ki opisuje vrsto problema. Ta stavek naj bo golo besedilo (brez LaTeXa, HTMLja, …), ki se bo prikazalo uporabnikom ob izbiri problema.
- Vsem parametrom je treba kot prvi argument podati niz s pravilnim prikazom imena (s šumniki in morebitnimi velikimi začetnicami).
- Vsem parametrom je treba podati argument `help_text` z besedilom, ki opisuje namen parametra.
- V podrazredu `Meta` je treba definirati spremenljivko `verbose_name` s pravilnim prikazom imena problema.
- Definirati metodo `generate`, ki vrne slovar podatkov, ki jih lahko kasneje uporabite v navodilu in rešitvi naloge.

V metodi `generate` naključne vrednosti izbirate s pomočjo funkcij iz knjižnice `random`. Za nastavitev semena generatorja psevdonaključnih števil vam ni treba skrbeti. Če želite v problemu delati s simbolnimi izrazi, uporabite knjižnico `sympy`. Če želite lepo rešitev, je običajno bolje, da generirate najprej rešitev in nato nalogo, na primer najprej ničle polinoma in iz njih koeficiente ter ne obratno. Včasih se to ne da in za generiranje lepe rešitve potrebujete več poskusov. V tem primeru uporabite izjemo `GeneratedDataIncorrect`, ki jo sprožite, kadar podatki niso ustrezni. V tem primeru bo program izbral novo seme generatorja ter nalogo poskusil sestaviti znova.

Potem ko uspešno napišete tak razred, poženite ukaza:

`python manage.py makemigrations`

`python manage.py migrate`

Tako posodobite vašo podatkovno bazo. Da pa bo stvar pravilno delovala, morate še prek adminskega vmesnika **dodati novo besedilo naloge, ki pripada temu razredu**. To storite pod "Problem texts + Dodaj". Za Content type izberite ustrezen `verbose_name`.
V besedilih navodila in rešitev smete uporabljati spremenljivke, ki jih generira posamezen razred naloge. To naredite z znakom @. Če hočete, da del besedila izgleda kot LaTeXa formula, besedilo vstavite med $$.

**Primer dodajanja besedila prek adminskega vmesnika**:

- _Content type_: (tukaj izberete ustrezno ime iz seznama)
- _Instruction_: "Dani sta števili \$@prvo_stevilo$ in \$@drugo_stevilo$. Poišči njuno vsoto!"
- _Solution_: "Njuna vsota je \$@vsota$.".

Še več konkretnih primerov lahko najdete na adminskem vmesniku pod "Problem texts"

**Opomba:** Trenutno besedil **ne** morete spreminjati prek python datotek, ampak samo prek adminskega vmesnika!!

Ko prek vmesnika dodate besedilo naloge, spremenite podatkovno bazo. Vendar ostane datoteka `nadlogar\problems\fixtures\initial.json` nespremenjena! Zato je treba v terminalu pognati naslednji ukaz (zagotovo dela za Windows):

`python -Xutf8 manage.py dumpdata --output 'problems\fixtures\initial.json' --indent 4`

Veliko problemov je v okviru svoje magistrske naloge že naredila _Urša Pertot_. Večina jih še ni implementiranih v Nadlogarja, so pa dostopni na [njenem repozitoriju](https://github.com/ursa16180/generiranje-nalog).

## Nekaj ne dela pravilno?!?

V tem primeru vprašanje lahko zastavite na [Discord kanalu programerskega krožka FMF](https://discord.gg/259nUehq), kjer v podzavihku _Nadlogar_ potekajo glavni pogovori glede projekta.
