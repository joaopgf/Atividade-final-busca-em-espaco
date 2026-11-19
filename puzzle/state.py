from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        filhos = []
        n = int(len(self.tiles) ** 0.5) 
        i = self.blank_index
        linha, coluna = i // n, i % n

        if linha != 0:
            nova = list(self.tiles)
            j = i - n
            nova[i], nova[j] = nova[j], nova[i]
            nova = tuple(nova)
            filho = State(nova, parent=self, action="UP", cost=self.cost + 1)
            filhos.append(filho)
            #print("pode ir para cima, troca com", i - n)
        if linha != n - 1:
            nova = list(self.tiles)
            j = i + n
            nova[i], nova[j] = nova[j], nova[i]
            nova = tuple(nova)
            filho = State(nova, parent=self, action="DOWN", cost=self.cost + 1)
            filhos.append(filho)
            #print("pode ir para baixo, troca com", i + n)
        if coluna != 0:
            nova = list(self.tiles)
            j = i - 1
            nova[i], nova[j] = nova[j], nova[i]
            nova = tuple(nova)
            filho = State(nova, parent=self, action="LEFT", cost=self.cost + 1)
            filhos.append(filho)
            #print("pode ir para a esquerda, troca com", i - 1)
        if coluna != n - 1:
            nova = list(self.tiles)
            j = i + 1
            nova[i], nova[j] = nova[j], nova[i]
            nova = tuple(nova)
            filho = State(nova, parent=self, action="RIGHT", cost=self.cost + 1)
            filhos.append(filho)
            #print("pode ir para a direita, troca com", i + 1)

        return filhos

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        # TODO: implemente a reconstrução do caminho usando self.parent
        raise NotImplementedError

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        # TODO: implemente usando path()
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
