# NAVODILA ZA OSNOVNO UPORABO NADLOGARJA

Tukaj se nahajajo osnovna navodila za uporabo Nadlogarja. Vsem, ki pri projektu nameravajo sodelovati ali kakorkoli pomagati, toplo priporočamo, da si jih preberejo.

## NAMESTITEV NADLOGARJA

Za namestitev Nadlogarja je potrebno upoštevati navodila, ki jih najdemo na [githubu](https://github.com/ul-fmf/nadlogar).
Nato gremo v mapo, ki vsebuje datoteko `manage.py` in poženemo ukaz `python manage.py loaddata documents/fixtures/initial.json`. To nam naloži nekaj koristinih latex predlog.

## KAKO POŽENEMO NADLOGARJA?

Če poženemo ukaz `python manage.py runserver`, nam na [lokalnem strežniku](http://127.0.0.1:8000) požene spletno stran. Vendar se moramo za njeno uporabo najprej prijaviti.
Zato ustvarimo adminskega uporabnika, kar storimo z ukazom `python manage.py createsuperuser`. Vendar pa to ni edina stran, ki nam je dostopna!
Uporabljamo lahko tudi [adminski vmesnik](http://127.0.0.1:8000/admin/), kjer med drugim dodajamo nova besedila nalog (vsaj zaenkrat, saj se bo shranjevanje besedil kmalu spremenilo).

## KAKO DODAMO NALOGO?

Najprej v ustrezni `.py` datoteki v mapi `nadlogar\problems\models` naredimo nov podrazred razreda `Problem`. Ta razred nujno potrebuje funkcijo `generate()` in string `verbose_name`, ki se nahaja znotraj razreda `Meta` (konkretne primere si lahko ogledate recimo v datoteki `nadlogar\problems\models\mnozice.py`).
Funkcija `generate()` generira slovar spremenljivk, ki jih nato smemo uporabljati v besedilih nalog (torej tako v navodilu kot v rešitvah). Spremenljivka `verbose_name `pa samo pove, pod katerim imenom bomo problem našli v adminskem vmesniku.
Potem ko uspešno napišemo tak razred, poženemo ukaza:

`python manage.py makemigrations`

`python manage.py migrate`

Tako posodobimo našo podatkovno bazo. Da pa bo stvar pravilno delovala, moramo še prek adminskega vmesnika **dodati novo besedilo naloge, ki pripada temu razredu**. To storimo pod "Problem texts + Dodaj". Za Content type izberemo ustrezen `verbose_name`.
V besedilih navodila in rešitev smemo uporabljati spremenljivke, ki jih generira
posamezen razred naloge. To naredimo z znakom @. Če hočemo, da del besedila izgleda kot latex formula, besedilo vstavimo med $$.

**Primer dodajanja besedila prek adminskega vmesnika**:

- _Content type_: (tukaj izberemo ustrezno ime iz seznama)
- _Instruction_: "Dani sta števili \$@prvo_stevilo$ in \$@drugo_stevilo$. Poišči njuno vsoto!"
- _Solution_: "Njuna vsota je \$@vsota$.".

Še več konkretnih primerov lahko najdemo na adminskem vmesniku pod "Problem texts"

**Opomba:** Trenutno besedil **ne** moremo spreminjati prek python datotek, ampak samo prek adminskega vmesnika!!

Ko prek vmesnika dodamo besedilo naloge, spremenimo podatkovno bazo. Vendar ostane datoteka `nadlogar\problems\fixtures\initial.json` nespremenjena! Zato je treba v terminalu pognati naslednji ukaz (zagotovo dela za Windows):

`python -Xutf8 manage.py dumpdata --output 'problems\fixtures\initial.json' --indent 4`

## KAJ ŠE VEDNO NE DELA?!?

V tem primeru (oziroma v vseh primerih) je zelo priporočen obisk [Discord skupine programerskega krožka](https://discord.gg/259nUehq), kjer tudi potekajo glavni pogovori glede projekta.
