import random

import sympy
from django.db import models

from .meta import GeneratedDataIncorrect, Problem

# Naloga z iskanjem ničel polinoma se skriva pod razno.py, verjetno jo bomo prestavili sem
# Grafa še ne bomo


class IzracunNicelVPrimeruDvojneNicle(Problem):
    """Problem, v katerem je treba poiskati ničle danega polinoma, pri čemer je neka ničla dvojna."""

    default_instruction = r"""Pokaži, da je število $@dvojna_nicla$ dvojna ničla polinoma $p(x)=@polinom$ in poišči še preostali ničli."""
    default_solution = r"""$x_3=@tretja_nicla$, $x_4=@cetrta_nicla$"""

    class Meta:
        verbose_name = "Polinomi / iskanje ničel v primeru dvojne ničle"

    def _poskusi_sestaviti(self):
        x = sympy.symbols("x")
        dvojna_nicla = random.choice(
            [-5, -4, -3, -2, -1, 2, 3, 4, 5]
        )  # Nočem da je dvojna nišla 0 ali 1 ker prelahko
        # Treba je generirati kvadratno funkcijo
        [a, b, c, splosna] = splosna_oblika()
        [tretja_nicla, cetrta_nicla] = nicle(a, b, c)

        if not (tretja_nicla != dvojna_nicla and cetrta_nicla != dvojna_nicla):
            raise GeneratedDataIncorrect

        polinom = sympy.expand(sympy.Mul((x - dvojna_nicla) ** 2, splosna))
        return {
            "polinom": polinom,
            "dvojna_nicla": dvojna_nicla,
            "tretja_nicla": tretja_nicla,
            "cetrta_nicla": cetrta_nicla,
        }
