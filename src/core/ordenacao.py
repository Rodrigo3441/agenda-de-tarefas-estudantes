from datetime import datetime

# =========================
# LIMITE DE TROCA DE ALGORITMO
# =========================
# Para listas pequenas, o Insertion Sort possui menor custo operacional.
# Acima de 10 elementos, o Merge Sort se torna mais eficiente.
LIMITE_INSERTION = 10


# =========================
# PESO DAS PRIORIDADES
# =========================
# Quanto menor o número, maior a prioridade.
def peso_prioridade(prioridade):

    prioridades = {
        "Alta": 1,
        "Media": 2,
        "Média": 2,
        "Baixa": 3
    }

    return prioridades.get(prioridade, 2)


# =========================
# COMPARAÇÃO ENTRE TAREFAS
# =========================
# Critérios:
# 1 - Data de entrega
# 2 - Prioridade
def tarefa_menor(tarefa1, tarefa2):

    # Compara primeiro pela data
    if tarefa1.data_entrega < tarefa2.data_entrega:
        return True

    if tarefa1.data_entrega > tarefa2.data_entrega:
        return False

    # Se a data for igual, compara prioridade
    prioridade1 = peso_prioridade(tarefa1.prioridade)
    prioridade2 = peso_prioridade(tarefa2.prioridade)

    return prioridade1 <= prioridade2


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

    # Compara elementos das duas listas
    while i < len(esquerda) and j < len(direita):

        if tarefa_menor(esquerda[i], direita[j]):

            resultado.append(esquerda[i])
            i += 1

        else:

            resultado.append(direita[j])
            j += 1

    # Adiciona elementos restantes
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

    # Começa do segundo elemento
    for i in range(1, len(tarefas)):

        atual = tarefas[i]
        j = i - 1

        # Move elementos maiores para frente
        while j >= 0 and not tarefa_menor(tarefas[j], atual):

            tarefas[j + 1] = tarefas[j]
            j -= 1

        # Insere elemento na posição correta
        tarefas[j + 1] = atual

    return tarefas


# =========================
# ORDENAÇÃO INTELIGENTE
# =========================
# Escolhe automaticamente o melhor algoritmo
# baseado na quantidade de tarefas.

def ordenar_tarefas(tarefas):

    # Para listas pequenas, o Insertion Sort é mais eficiente
    if len(tarefas) < LIMITE_INSERTION:

        print("Usando Insertion Sort")

        return insertion_sort(tarefas)

    # Para listas maiores, o Merge Sort possui melhor desempenho
    else:

        print("Usando Merge Sort")

        return merge_sort(tarefas)


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

            # Converte a data da tarefa
            data_tarefa = datetime.strptime(
                str(tarefa.data_entrega),
                "%Y-%m-%d"
            ).date()

            # Calcula diferença em dias
            diferenca = (data_tarefa - hoje).days

            # Marca tarefa como vencida
            tarefa.vencida = diferenca < 0

            # =========================
            # REGRAS DE NOTIFICAÇÃO
            # =========================

            # Tarefa vencida
            if diferenca < 0:

                notificacoes.append(
                    f'⚠️ "{tarefa.titulo}" está vencida! Recomenda-se excluir ou atualizar.'
                )

            # Vence hoje
            elif diferenca == 0:

                notificacoes.append(
                    f'URGENTE! "{tarefa.titulo}" vence hoje!'
                )

            # Vence amanhã
            elif diferenca == 1:

                notificacoes.append(
                    f'Atenção! "{tarefa.titulo}" vence amanhã!'
                )

    # Retorna notificações geradas
    return notificacoes