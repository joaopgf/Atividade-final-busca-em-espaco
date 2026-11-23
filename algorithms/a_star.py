import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma, para cada peça, quantas casas ela está do seu lugar."""
        n = int(len(state.tiles) ** 0.5)  # tamanho do lado do tabuleiro (3)
        total = 0

        # enumerate devolve a posição (i) e o valor da peça (v) ao mesmo tempo
        for i, v in enumerate(state.tiles):
            # o vazio não conta: contar ele superestimaria o custo (heurística deixaria de ser admissível)
            if v == 0:
                continue

            destino = GOAL_STATE.index(v)  # posição onde a peça v deveria estar

            # transforma as posições em (linha, coluna), igual ao neighbors()
            linha_atual, coluna_atual = i // n, i % n
            linha_dest, coluna_dest = destino // n, destino % n

            # |x1 - x2| + |y1 - y2| 
            total += abs(linha_atual - linha_dest) + abs(coluna_atual - coluna_dest)

        return total

    def search(self, initial: State) -> SearchResult:
        # contador de desempate: se dois nós tiverem o mesmo f, sai primeiro o que entrou antes
        contador = 0

        # fronteira = fila de prioridade (heap). Cada item é (f, contador, estado).
        # O heapq sempre tira o item de menor f primeiro.
        fronteira = [(self.heuristic(initial), contador, initial)]

        # melhor custo g já encontrado para cada tabuleiro
        melhor_g = {initial: 0}

        expandidos = 0
        gerados = 0
        max_fronteira = 1

        while fronteira:
            # tira o nó com menor f(n) = g(n) + h(n)
            f, _, no = heapq.heappop(fronteira)

            # se já achamos um caminho mais barato para este tabuleiro, esta entrada é velha: ignora
            if no.cost > melhor_g[no]:
                continue

            # o objetivo é testado ao tirar da fronteira (é isso que garante o caminho ótimo)
            if no.is_goal:
                return SearchResult(
                    solution=no,
                    nodes_expanded=expandidos,
                    nodes_generated=gerados,
                    max_frontier_size=max_fronteira,
                    depth=no.cost,
                )

            # expande o nó: gera os filhos
            filhos = no.neighbors()
            expandidos += 1
            gerados += len(filhos)

            for filho in filhos:
                # só entra se for um tabuleiro novo ou se chegamos nele por um caminho mais barato
                if filho not in melhor_g or filho.cost < melhor_g[filho]:
                    melhor_g[filho] = filho.cost
                    contador += 1
                    f_filho = filho.cost + self.heuristic(filho)  # f(n) = g(n) + h(n)
                    heapq.heappush(fronteira, (f_filho, contador, filho))

            max_fronteira = max(max_fronteira, len(fronteira))

        # fronteira vazia sem achar o objetivo: não há solução
        return SearchResult(solution=None, nodes_expanded=expandidos,
                            nodes_generated=gerados, max_frontier_size=max_fronteira)
