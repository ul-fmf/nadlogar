import random

import sympy
from django.db import models

from .meta import GeneratedDataIncorrect, Problem


def generiraj_kompleksna_stevila(kolicina):
    stevila_r = random.choices(
        [x for x in range(-5, 6) if x != 0],
        k=kolicina,  # Izbere naključne realne dele
    )
    stevila_i = random.choices(
        [x for x in range(-5, 6) if x != 0],
        k=kolicina,  # Izbere naključne imaginarne dele
    )
    stevila = [r + i * sympy.I for r, i in zip(stevila_r, stevila_i)]

    if len(stevila) != len(
        set(stevila)
    ):  # preveri, da so vsa števila medsebojno različna
        raise GeneratedDataIncorrect

    if kolicina == 1:
        stevila = stevila[0]

    return stevila


class VsotaKompleksnih(Problem):
    """Problem za seštevanje in odštevanje kompleksnih števil."""

    default_instruction = "Izračunaj $z=@izraz$."
    default_solution = "$z=@resitev$"

    class Meta:
        verbose_name = "Kompleksna števila / seštevanje in odštevanje ulomkov"

    def generate(self):
        kolicina = 3
        koeficienti_s = random.choices(
            range(1, 5),
            weights=(3, 1, 1, 1),
            k=kolicina,  # Izbere naključne števce, prednost ima 1
        )
        koeficienti_i = random.choices(
            range(1, 5),
            weights=(7, 1, 1, 1),
            k=kolicina,  # Izbere naključne imenovalce, prednost ima 1
        )
        koeficienti_p = random.choices(
            (-1, 1),
            weights=(1, 2),
            k=kolicina,  # Izbere naključne predznake, prednost ima pozitiven
        )
        koeficienti = [
            p * sympy.Rational(s, i)
            for p, s, i in zip(koeficienti_p, koeficienti_s, koeficienti_i)
        ]

        stevila = generiraj_kompleksna_stevila(kolicina)

        izraz = sympy.Add(
            *[sympy.Mul(k, z, evaluate=False) for k, z in zip(koeficienti, stevila)],
            evaluate=False,
        )
        resitev = sympy.simplify(izraz)

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class KompleksniUlomek(Problem):
    """Problem za seštevanje in racionalizacijo kompleksnih ulomkov."""

    default_instruction = "Izračunaj $z=@izraz$."
    default_solution = "$z=@resitev$"

    class Meta:
        verbose_name = "Kompleksna števila / seštevanje in racionalizacija ulomkov"

    def generate(self):
        kolicina = 4
        stevila = generiraj_kompleksna_stevila(kolicina)

        izraz = sympy.Add(
            sympy.Mul(
                stevila[0], sympy.Pow(stevila[1], -1, evaluate=False), evaluate=False
            ),
            sympy.Mul(
                stevila[2], sympy.Pow(stevila[3], -1, evaluate=False), evaluate=False
            ),
            evaluate=False,
        )
        resitev = sympy.simplify(izraz)

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class MnozenjeKompleksnih(Problem):
    """Problem za množenje kompleksnih števil."""

    default_instruction = "Izračunaj $z=@izraz$."
    default_solution = "$z=@resitev$"

    class Meta:
        verbose_name = "Kompleksna števila / množenje"

    def generate(self):
        kolicina = 2
        stevila = generiraj_kompleksna_stevila(kolicina)

        izraz = sympy.Mul(*stevila, evaluate=False)
        resitev = sympy.simplify(izraz)

        return {
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class RacunanjeKompleksno(Problem):
    """Problem za računanje absolutne vrednosti, potenciranja in konjugiranje kompleksnega števila ter višje potence kompleksne enote i."""

    default_instruction = (
        "Dano je kompleksno število $z=@stevilo$. Izračunaj število $w=@izraz$."
    )
    default_solution = "$w=@resitev$"

    class Meta:
        verbose_name = "Kompleksna števila / računanje s kompleksno enoto"

    def generate(self):
        z = sympy.symbols("z")
        z0 = generiraj_kompleksna_stevila(1)
        izraz = (
            sympy.Pow(z, random.randint(2, 3))
            + sympy.Mul(
                sympy.Pow(sympy.I, random.randint(1991, 2018), evaluate=False),
                sympy.conjugate(z),
                evaluate=False,
            )
            + abs(z) ** 2
        )
        resitev = sympy.simplify(izraz.subs(z, z0))
        return {
            "stevilo": sympy.latex(z0),
            "izraz": sympy.latex(izraz),
            "resitev": sympy.latex(resitev),
        }


class KompleksnaEnacba(Problem):
    """Problem za množenja, konjugiranja, absolutne vrednosti in komponent kompleksnih števil."""

    default_instruction = "Katero kompleksno število $z$ zadošča enačbi $@enacba$? Zapiši $\\operatorname{Re}(z)$ in $\\operatorname{Im}(z)$ ter izračunaj $\\left| z \\right|$."
    default_solution = "$z=@resitev$, $\\operatorname{Re}(z)=@realna$, $\\operatorname{Im}(z)=@imaginarna$, $\\left|z\\right|=@absolutna$"

    konjugirana_vrednost = models.BooleanField(
        "konjugirana vrednost",
        help_text="Ali naj naloga vsebuje konjugirano vrednost?",
        choices=[(True, "Da"), (False, "Ne")],
        default=True,
    )

    class Meta:
        verbose_name = "Kompleksna števila / reševanje enačb s kompleksnimi števili"

    def generate(self):
        z = sympy.symbols("z")
        resitev, z1 = generiraj_kompleksna_stevila(2)
        if not self.konjugirana_vrednost:
            enacba = z1 * z
        else:
            z2 = generiraj_kompleksna_stevila(1)
            enacba = z1 * z + z2 * sympy.conjugate(z)
        z3 = sympy.simplify(enacba.subs(z, resitev))
        im = sympy.im(resitev)
        re = sympy.re(resitev)
        absolutna = abs(resitev)

        return {
            "enacba": sympy.latex(sympy.Eq(enacba, z3)),
            "resitev": sympy.latex(resitev),
            "imaginarna": sympy.latex(im),
            "realna": sympy.latex(re),
            "absolutna": sympy.latex(absolutna),
        }


class NarisiKompleksna(Problem):
    """Problem za risanje kompleksnih števil v kompleksno ravnino."""

    default_instruction = "V kompleksno ravnino nariši števila $z_1=@stevila[0]$, $z_2=@stevila[1]$, $z_3=@stevila[2]$ in $z_4=@stevila[3]$."
    default_solution = "$z_1=@koordinate[0]$, $z_2=@koordinate[1]$, $z_3=@koordinate[2]$ in $z_4=@koordinate[3]$"

    class Meta:
        verbose_name = "??? / risanje v ravnino"

    def generate(self):
        kolicina = 4
        stevila = generiraj_kompleksna_stevila(kolicina)
        koordinate = ["({0}, {1})".format(sympy.re(z), sympy.im(z)) for z in stevila]
        return {"stevila": [sympy.latex(z) for z in stevila], "koordinate": koordinate}
