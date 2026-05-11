from datetime import datetime

# =========================
# MERGE SORT
# =========================
# Algoritmo de ordenação eficiente baseado no conceito de "dividir para conquistar"
# Complexidade: O(n log n)
# Usado quando há muitas tarefas, pois é mais rápido em grandes volumes de dados.

def merge_sort(tarefas):

    # Caso base: se a lista tiver 0 ou 1 elemento, já está ordenada
    if len(tarefas) <= 1:
        return tarefas

    # Divide a lista ao meio
    meio = len(tarefas) // 2

    # Chamada recursiva para ordenar a parte esquerda e direita
    esquerda = merge_sort(tarefas[:meio])
    direita = merge_sort(tarefas[meio:])

    # Junta as duas partes ordenadas
    return merge(esquerda, direita)


# =========================
# FUNÇÃO AUXILIAR DO MERGE SORT
# =========================
# Responsável por combinar duas listas já ordenadas em uma única lista ordenada

def merge(esquerda, direita):

    resultado = []

    i = 0  # índice da lista esquerda
    j = 0  # índice da lista direita

    # Compara elementos das duas listas e organiza pela data de entrega
    while i < len(esquerda) and j < len(direita):

        # Ordenação baseada na data de entrega (mais próxima primeiro)
        if esquerda[i].data_entrega < direita[j].data_entrega:

            resultado.append(esquerda[i])
            i += 1

        else:

            resultado.append(direita[j])
            j += 1

    # Adiciona o restante dos elementos que não foram comparados
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado


# =========================
# INSERTION SORT
# =========================
# Algoritmo simples de ordenação
# Melhor desempenho em listas pequenas
# Complexidade: O(n²)

def insertion_sort(tarefas):

    # Começa do segundo elemento (índice 1)
    for i in range(1, len(tarefas)):

        atual = tarefas[i]  # elemento que será inserido na posição correta
        j = i - 1

        # Move elementos maiores para frente
        while j >= 0 and tarefas[j].data_entrega > atual.data_entrega:

            tarefas[j + 1] = tarefas[j]
            j -= 1

        # Insere o elemento na posição correta
        tarefas[j + 1] = atual

    return tarefas


# =========================
# VERIFICAÇÃO DE PRAZOS
# =========================
# Gera notificações automáticas baseadas na proximidade da data de entrega

def verificar_prazos(tarefas):

    notificacoes = []

    # Data atual do sistema
    hoje = datetime.today().date()

    for tarefa in tarefas:

        if tarefa.data_entrega:

            # Converte a data da tarefa para formato de data
            data_tarefa = datetime.strptime(
                str(tarefa.data_entrega),
                "%Y-%m-%d"
            ).date()

            # Calcula diferença de dias entre hoje e a entrega
            diferenca = (data_tarefa - hoje).days

            # =========================
            # REGRAS DE NOTIFICAÇÃO
            # =========================

            # Se vence hoje
            if diferenca == 0:
                notificacoes.append(
                    f'URGENTE! "{tarefa.titulo}" vence hoje!'
                )

            # Se vence amanhã
            elif diferenca == 1:
                notificacoes.append(
                    f'Atenção! "{tarefa.titulo}" vence amanhã!'
                )

    # Retorna lista de alertas gerados
    return notificacoes