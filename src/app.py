from urllib.parse import quote_plus
from flask import Flask, render_template, request, redirect
from database.db import db
from database.models import Tarefa
from service.tarefa_service import criar_tarefa, criar_tarefas_de_arquivo
from core.undo_stack import UndoStack
from core.fila_notificacao import FilaNotificacao
from core.ordenacao import (
    merge_sort, 
    insertion_sort, 
    verificar_prazos
)

# =========================
# INICIALIZAÇÃO DO FLASK
# =========================
# Aqui criamos a aplicação Flask e configuramos a conexão com o banco MySQL
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/agenda_academica"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o banco de dados na aplicação
db.init_app(app)

# =========================
# ESTRUTURAS DE DADOS (RECURSOS DO PROJETO)
# =========================
# Pilha usada para desfazer ações (LIFO - Last In, First Out)
undo_stack = UndoStack()

# Fila usada para gerenciar notificações (FIFO - First In, First Out)
fila_notificacao = FilaNotificacao()

# =========================
# CARREGAMENTO E ORGANIZAÇÃO DE DADOS
# =========================
def _carregar_estado_telas():
    # Busca todas as tarefas no banco de dados
    tarefas = list(Tarefa.query.all())
    
    # Escolha do algoritmo de ordenação baseada no tamanho da lista
    # Isso demonstra preocupação com complexidade (Big-O)
    if len(tarefas) < 10:
        tarefas_ordenadas = insertion_sort(tarefas)  # melhor para listas pequenas
    else:
        tarefas_ordenadas = merge_sort(tarefas)  # mais eficiente para listas grandes
    
    # Verifica prazos das tarefas e gera avisos
    avisos_prazo = verificar_prazos(tarefas_ordenadas)
    
    # Limpa fila antes de atualizar notificações
    fila_notificacao.fila.clear()
    
    # Adiciona novos avisos na fila
    for aviso in avisos_prazo:
        fila_notificacao.enqueue(aviso)
    
    # Retorna notificações para exibição na interface
    notificacoes = fila_notificacao.visualizar()
    return tarefas_ordenadas, notificacoes

# =========================
# FUNÇÃO AUXILIAR DE REDIRECIONAMENTO
# =========================
# Evita repetição de código ao enviar mensagens para o usuário
def _redirect_resultado(mensagem, tipo="sucesso"):
    mensagem_param = quote_plus(mensagem)
    tipo_param = quote_plus(tipo)
    return redirect(f"/resultado?mensagem={mensagem_param}&tipo={tipo_param}")

# =========================
# ROTAS PRINCIPAIS
# =========================

# Página inicial da aplicação
@app.route("/")
def home():
    tarefas_ordenadas, notificacoes = _carregar_estado_telas()
    return render_template(
        "index.html",
        tarefas=tarefas_ordenadas,
        notificacoes=notificacoes,
        feedback=request.args.get("feedback", "")
    )

# Página de resultado após ações do sistema
@app.route("/resultado")
def resultado():
    tarefas_ordenadas, notificacoes = _carregar_estado_telas()
    return render_template(
        "resultado.html",
        tarefas=tarefas_ordenadas,
        notificacoes=notificacoes,
        mensagem=request.args.get("mensagem", ""),
        tipo=request.args.get("tipo", "sucesso"),
    )

# =========================
# CRIAÇÃO DE TAREFAS
# =========================
@app.route("/criar", methods=["POST"])
def criar_tarefa_route():
    # Cria uma nova tarefa com base nos dados do formulário
    nova_tarefa = criar_tarefa(request.form)
    
    # Salva ação na pilha para permitir desfazer depois
    undo_stack.push({
        "tipo": "criar",
        "id": nova_tarefa.id
    })
    
    # Adiciona notificação na fila
    fila_notificacao.enqueue("Tarefa criada com sucesso!")
    return _redirect_resultado("Tarefa criada com sucesso!")

# =========================
# IMPORTAÇÃO DE TAREFAS
# =========================
@app.route("/importar", methods=["POST"])
def importar_tarefas_route():
    arquivo = request.files.get("arquivo_tarefas")
    
    # Validação simples: verifica se arquivo foi enviado
    if arquivo is None:
        return _redirect_resultado("Nenhum arquivo foi enviado.", "erro")
    
    try:
        # Cria várias tarefas a partir de um arquivo externo
        total = criar_tarefas_de_arquivo(arquivo)
        
        fila_notificacao.enqueue(f"{total} tarefa(s) importada(s) com sucesso!")
        return _redirect_resultado(f"Importação concluída. {total} tarefas adicionadas.")
    
    except ValueError as exc:
        return _redirect_resultado(str(exc), "erro")

# =========================
# EDIÇÃO DE TAREFAS
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    
    if tarefa is None:
        return _redirect_resultado("Tarefa não encontrada.", "erro")
    
    if request.method == "POST":
        # Salva estado atual antes de editar (para permitir desfazer)
        undo_stack.push({
            "tipo": "editar",
            "id": tarefa.id,
            "titulo_antigo": tarefa.titulo,
            "descricao_antiga": tarefa.descricao,
            "data_antiga": tarefa.data_entrega,
            "prioridade_antiga": tarefa.prioridade
        })
        
        # Atualiza os dados da tarefa
        tarefa.titulo = request.form.get("titulo")
        tarefa.descricao = request.form.get("descricao")
        tarefa.data_entrega = request.form.get("data_entrega")
        tarefa.prioridade = request.form.get("prioridade")
        
        db.session.commit()
        fila_notificacao.enqueue("Tarefa editada com sucesso!")
        
        return _redirect_resultado("Tarefa editada com sucesso!")
    
    return render_template("editar.html", tarefa=tarefa)

# =========================
# DESFAZER AÇÕES (UNDO STACK)
# =========================
@app.route("/desfazer")
def desfazer():
    # Remove última ação da pilha
    ultima_acao = undo_stack.pop()
    
    if ultima_acao is None:
        return _redirect_resultado("Nada para desfazer.", "erro")

    try:
        # Reverte edição
        if ultima_acao["tipo"] == "editar":
            tarefa = Tarefa.query.get(ultima_acao["id"])
            if tarefa:
                tarefa.titulo = ultima_acao["titulo_antigo"]
                tarefa.descricao = ultima_acao["descricao_antiga"]
                tarefa.data_entrega = ultima_acao["data_antiga"]
                tarefa.prioridade = ultima_acao["prioridade_antiga"]
        
        # Reverte criação (remove a tarefa)
        elif ultima_acao["tipo"] == "criar":
            tarefa = Tarefa.query.get(ultima_acao["id"])
            if tarefa:
                db.session.delete(tarefa)

        # Reverte exclusão (restaura tarefa)
        elif ultima_acao["tipo"] == "excluir":
            tarefa_restaurada = Tarefa(
                titulo=ultima_acao["titulo"],
                descricao=ultima_acao["descricao"],
                data_entrega=ultima_acao["data"],
                prioridade=ultima_acao["prioridade"]
            )
            db.session.add(tarefa_restaurada)

        db.session.commit()
        return _redirect_resultado("Ação desfeita com sucesso!")
    
    except Exception as e:
        db.session.rollback()
        return _redirect_resultado(f"Erro ao desfazer: {str(e)}", "erro")

# =========================
# EXCLUSÃO DE TAREFAS
# =========================
@app.route("/excluir/<int:id>")
def excluir_tarefa(id):
    tarefa = Tarefa.query.get(id)
    
    if tarefa is None:
        return _redirect_resultado("Tarefa não encontrada.", "erro")
    
    # Salva dados antes de excluir (para poder restaurar depois)
    undo_stack.push({
        "tipo": "excluir",
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "data": tarefa.data_entrega,
        "prioridade": tarefa.prioridade
    })
    
    db.session.delete(tarefa)
    db.session.commit()
    
    fila_notificacao.enqueue("Tarefa excluída com sucesso!")
    return _redirect_resultado("Tarefa excluída com sucesso.")

# =========================
# EXECUÇÃO DO PROJETO
# =========================
if __name__ == "__main__":
    # Cria tabelas automaticamente se não existirem
    with app.app_context():
        db.create_all()
    
    # Inicia servidor em modo debug
    app.run(debug=True)