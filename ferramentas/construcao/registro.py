"""Registro de ocupação: nada nasce sobre outro objeto (erro E-16) e anéis de passagem ficam livres (E-15).

    from construcao.registro import Ocupacao, retangulo, disco
    oc = Ocupacao()
    oc.reservar("casa", retangulo(10, 10, 20, 18))             # solido; colisão fica em oc.conflitos
    oc.reservar("anel_fonte", disco(30, 30, 7, 4), "anel")      # anel: precisa ficar livre para andar
    if oc.livre([(x, z)]): ...                                  # antes de colocar poste/árvore/etc.
Regra: base de objetos de chão = altura do TERRENO H, nunca "o bloco mais alto da coluna" (Cena.chao) — senão nasce sobre telhado/toldo (E-14).
"""
import math


def retangulo(x1, z1, x2, z2):
    return [(x, z) for x in range(x1, x2 + 1) for z in range(z1, z2 + 1)]


def disco(cx, cz, r1, r2=0.0):
    """Células com r2 < distância <= r1 ao centro (r2 > 0 gera um anel)."""
    return [(x, z) for x in range(int(cx - r1) - 1, int(cx + r1) + 2) for z in range(int(cz - r1) - 1, int(cz + r1) + 2)
            if r2 < math.hypot(x - cx, z - cz) <= r1]


class Ocupacao:
    def __init__(self, W=None, D=None, bloqueadas=None):
        self.res = {}                 # (x,z) -> (dono, tipo) com tipo "solido" ou "anel"
        self.conflitos = []           # (dono_novo, dono_existente, célula)
        self.W, self.D = W, D
        self.bloqueadas = set(bloqueadas or ())   # células proibidas (ex.: água, caminhos)

    def livre(self, cels):
        return all((self.W is None or (0 <= x < self.W)) and (self.D is None or (0 <= z < self.D)) and (x, z) not in self.res and (x, z) not in self.bloqueadas
                   for (x, z) in cels)

    def reservar(self, dono, cels, tipo="solido", estrito=True):
        ok = True
        for k in cels:
            if k in self.res and self.res[k][0] != dono:
                ok = False
                if estrito:
                    self.conflitos.append((dono, self.res[k][0], k))
            else:
                self.res[k] = (dono, tipo)
        return ok

    def solido(self, cel):
        return cel in self.res and self.res[cel][1] == "solido"
