# =========================
# ESTRUTURA: FILA DE NOTIFICAÇÕES
# =========================
# Essa classe implementa uma fila simples (FIFO - First In, First Out)
# Ela é usada para armazenar mensagens do sistema, como avisos e confirmações.

class FilaNotificacao:

    # =========================
    # CONSTRUTOR DA CLASSE
    # =========================
    def __init__(self):
        # Inicializa a fila como uma lista vazia
        self.fila = []

    # =========================
    # INSERÇÃO NA FILA (enqueue)
    # =========================
    def enqueue(self, mensagem):
        # Adiciona uma nova mensagem ao final da fila
        # Ou seja, ela entra "por trás"
        self.fila.append(mensagem)

    # =========================
    # REMOÇÃO DA FILA (dequeue)
    # =========================
    def dequeue(self):

        # Verifica se a fila NÃO está vazia antes de remover
        if not self.esta_vazia():
            # Remove o primeiro elemento da fila (posição 0)
            # Isso garante o comportamento FIFO
            return self.fila.pop(0)

        # Se estiver vazia, retorna None
        return None

    # =========================
    # VERIFICA SE A FILA ESTÁ VAZIA
    # =========================
    def esta_vazia(self):
        # Retorna True se não houver elementos na fila
        return len(self.fila) == 0

    # =========================
    # VISUALIZAÇÃO DA FILA
    # =========================
    def visualizar(self):
        # Retorna todos os elementos da fila sem removê-los
        # Usado para exibir notificações na interface
        return self.fila