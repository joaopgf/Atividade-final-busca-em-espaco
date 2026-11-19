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
        visitados = {initial}
        expandidos = 0
        gerados = 0
        max_fronteira = 1

        while fronteira:
            #por ser uma fila o pop já basta ao invés do popleft
            no = fronteira.pop()

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
                if filho not in visitados:
                    visitados.add(filho)
                    fronteira.append(filho)

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(solution=None, nodes_expanded=expandidos,
                            nodes_generated=gerados, max_frontier_size=max_fronteira)
