from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        #define variável da fronteira, precisa de deque pelos métodos de manipulação do começo e fim da lista
        fronteira = deque([initial]) #[initial] é lista com um elemento que o deque exige

        #conjunto (set) com um elemento para melhor performance na busca
        visitados = {initial}
        expandidos = 0
        gerados = 0
        max_fronteira = 1

        #enquanto a fila não estiver vazia
        while fronteira:
            #retira o nó mais antigo e "entrega" ele para a variável
            no = fronteira.popleft()

            if no.is_goal:
                return SearchResult(
                    solution=no, #nó do objetivo
                    nodes_expanded=expandidos,
                    nodes_generated=gerados,
                    max_frontier_size=max_fronteira,
                    depth=no.cost,                 
                )

            #expande o nó: gera os filhos a partir dele
            filhos = no.neighbors()
            expandidos += 1                 
            gerados += len(filhos) 

            #percorre cada filho gerado, um por vez
            for filho in filhos:
                #só aceita tabuleiros que nunca apareceram (evita andar em círculos)
                if filho not in visitados:
                    visitados.add(filho)#marca como já visto
                    fronteira.append(filho)#entra no fim da fila para ser expandido depois

            #escolhe entre o recorde atual e o novo como fronteira máxima
            max_fronteira = max(max_fronteira, len(fronteira))

        #se não achar resultado volta solution=None
        return SearchResult(solution=None, nodes_expanded=expandidos,
                            nodes_generated=gerados, max_frontier_size=max_fronteira)
