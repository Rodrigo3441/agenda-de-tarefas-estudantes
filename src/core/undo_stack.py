# =========================
# ESTRUTURA: PILHA DE DESFAZER (UNDO STACK)
# =========================
# Essa classe implementa uma pilha (LIFO - Last In, First Out)
# Ela é usada para armazenar ações do sistema para permitir o "desfazer"

class UndoStack:

    # =========================
    # INICIALIZAÇÃO DA PILHA
    # =========================
    def __init__(self):
        # Cria uma lista vazia que será usada como pilha
        self.pilha = []

    # =========================
    # PUSH (EMPILHAR AÇÃO)
    # =========================
    def push(self, acao):
        # Adiciona uma nova ação no topo da pilha
        # Sempre a última ação fica no topo (LIFO)
        self.pilha.append(acao)

    # =========================
    # POP (DESFAZER AÇÃO)
    # =========================
    def pop(self):

        # Verifica se a pilha não está vazia antes de remover
        if not self.esta_vazia():

            # Remove e retorna o último elemento inserido
            # Isso garante o comportamento LIFO
            return self.pilha.pop()

        # Se não houver nada para desfazer
        return None

    # =========================
    # VERIFICA SE A PILHA ESTÁ VAZIA
    # =========================
    def esta_vazia(self):
        # Retorna True se não houver elementos na pilha
        return len(self.pilha) == 0

    # =========================
    # VISUALIZAÇÃO DA PILHA
    # =========================
    def visualizar(self):
        # Retorna todas as ações armazenadas sem removê-las
        return self.pilha