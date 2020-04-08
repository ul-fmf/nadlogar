# Nadlogar

Nadlogar je spletna storitev za generiranje naključnih nalog ter njihovih rešitev. Učitelj izbere seznam tipskih nalog in vzorčno izhodno datoteko ter naloži seznam učencev, storitev pa za vsakega učenca ustvari posamezne datoteke z nalogami ter skupno datoteko z rešitvami. Naloge niso čisto naključne, saj storitev za istega učenca vedno vrne enako nalogo, kar omogoča, da naloge naknadno popravljate, ne da bi se vam pri tem v celoti spremenile.

Nadlogar je projekt, ki nastaja v okviru programerskega kluba [Fakultete za matematiko in fiziko, Univerza v Ljubljani](http://www.fmf.uni-lj.si/). Poleg vseh članov kluba, ki k razvoju prispevajo vse od idej do kode, so k razvoju bistveno pomagali oziroma še pomagajo:

- Gregor Šega, ki je napisal prvo skripto za generiranje nalog v _Mathematici_ in s tem dal idejo za splošen program,
- Matija Pretnar, ki je na osnovi te skripte v _Mathematici_ napisal [splošen program](https://github.com/matijapretnar/generiranje-nalog),
- Urša Pertot, ki je na osnovi tega programa napisala [program v Pythonu](https://github.com/ursa16180/generiranje-nalog/tree/python),
- podjetje [EBA d.o.o., Ljubljana](http://www.ebadms.com), ki je velikodušno prevzelo sponzorstvo programerskega kluba.

## Navodila za namestitev

Na začetku klonirajte repozitorij ter ustvarite virtualno okolje:

    git clone git@github.com:ul-fmf/nadlogar.git
    cd nadlogar
    python3 -m venv venv

Dobiti bi morali sledečo strukturo datotek:

    nadlogar/
        nadlogar/
            config/
            naloge/
            ...
        manage.py
        ...
        venv/
            ...

Po prvi namestitvi, pa tudi na vsake toliko časa, greste v mapo `nadlogar/nadlogar/` in s sledečimi ukazi kodo posodobite, aktivirate virtualno okolje, namestite potrebne pakete ter posodobite bazo:

    git pull
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate

Če uporabljate Windowse, je drugi ukaz drugačen

    git pull
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate

Strežnik nato poženete z

    python manage.py runserver

Teste poženete z

    python manage.py test
