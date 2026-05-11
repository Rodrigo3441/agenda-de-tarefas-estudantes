import sys
from pathlib import Path

# =========================
# AJUSTE DE CAMINHO DO PROJETO
# =========================
# Aqui estamos adicionando a pasta "src" ao caminho do Python
# Isso permite importar módulos do projeto corretamente durante os testes

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from core.fila_notificacao import FilaNotificacao


# =========================
# TESTE 1: ENQUEUE E DEQUEUE (CASO BÁSICO)
# =========================
# Verifica se a fila adiciona e remove corretamente um único elemento

def test_enqueue_e_dequeue_caso_base():

    fila = FilaNotificacao()

    # Adiciona uma mensagem na fila
    fila.enqueue("mensagem 1")

    # Remove e verifica se é a mesma mensagem (FIFO)
    assert fila.dequeue() == "mensagem 1"


# =========================
# TESTE 2: FILA VAZIA
# =========================
# Verifica comportamento quando a fila está vazia

def test_dequeue_em_fila_vazia_retorna_none():

    fila = FilaNotificacao()

    # Ao tentar remover de uma fila vazia, deve retornar None
    assert fila.dequeue() is None

    # Confirma que a fila realmente está vazia
    assert fila.esta_vazia() is True


# =========================
# TESTE 3: MÚLTIPLOS ELEMENTOS (FIFO)
# =========================
# Garante que a ordem de saída respeita FIFO (First In, First Out)

def test_multiplos_elementos_respeitam_fifo():

    fila = FilaNotificacao()

    # Inserção de múltiplos elementos
    fila.enqueue("primeira")
    fila.enqueue("segunda")
    fila.enqueue("terceira")

    # A saída deve seguir a ordem de entrada
    assert fila.dequeue() == "primeira"
    assert fila.dequeue() == "segunda"
    assert fila.dequeue() == "terceira"