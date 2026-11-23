from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        #por ser lista um vetor comum ao invés de deque basta
        fronteira = [initial]

        #dicionário: tabuleiro -> menor profundidade em que ele já apareceu
        #(um set só diria "já vi"; aqui também sabemos "a que profundidade")
        visitados = {initial: 0}
        expandidos = 0
        gerados = 0
        max_fronteira = 1

        while fronteira:
            #por ser uma pilha o pop já basta ao invés do popleft
            no = fronteira.pop()

            #se esse tabuleiro já foi alcançado por um caminho mais raso, esta entrada é velha: ignora
            if no.cost > visitados[no]:
                continue

            if no.is_goal:
                return SearchResult(
                    solution=no, #nó do objetivo
                    nodes_expanded=expandidos,
                    nodes_generated=gerados,
                    max_frontier_size=max_fronteira,
                    depth=no.cost,                 
                )

            #verifica se a profundidade atingiu o limite
            if no.cost >= self.depth_limit:
                continue

            filhos = no.neighbors()
            expandidos += 1
            gerados += len(filhos)

            for filho in filhos:
                #aceita se o tabuleiro é novo ou se agora chegamos nele por um caminho mais raso
                #(com um set global, um tabuleiro visto primeiro perto do limite bloqueava o caminho curto)
                if filho not in visitados or filho.cost < visitados[filho]:
                    visitados[filho] = filho.cost
                    fronteira.append(filho)

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(solution=None, nodes_expanded=expandidos,
                            nodes_generated=gerados, max_frontier_size=max_fronteira)
