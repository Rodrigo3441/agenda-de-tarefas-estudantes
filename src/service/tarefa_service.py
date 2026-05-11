import csv
import io
import json

from database.db import db
from database.models import Tarefa
from core.undo_stack import UndoStack

# Instância da pilha para permitir desfazer ações
undo_stack = UndoStack()

# =========================
# CRIAÇÃO DE UMA TAREFA
# =========================
def criar_tarefa(dados):
    # Cria um objeto Tarefa a partir dos dados recebidos do formulário
    nova_tarefa = Tarefa(
        titulo=dados.get("titulo"),
        descricao=dados.get("descricao"),
        data_entrega=dados.get("data_entrega"),
        prioridade=dados.get("prioridade")
    )

    # Adiciona no banco de dados
    db.session.add(nova_tarefa)
    db.session.commit()

    # Retorna a tarefa criada
    return nova_tarefa

    # OBS: Esse trecho abaixo nunca será executado por causa do return
    # (fica aqui apenas como tentativa de registrar ação na pilha)
    undo_stack.push({
        "acao": "criar",
        "titulo": nova_tarefa.titulo
    })


# =========================
# IMPORTAÇÃO DE TAREFAS POR ARQUIVO
# =========================
def criar_tarefas_de_arquivo(file_storage):

    # Valida nome do arquivo
    filename = (file_storage.filename or "").strip()

    if not filename:
        raise ValueError("Selecione um arquivo para importar.")

    if "." not in filename:
        raise ValueError("Formato de arquivo invalido.")

    # Identifica extensão do arquivo
    extensao = filename.rsplit(".", 1)[1].lower()

    # Lê o conteúdo do arquivo
    conteudo = file_storage.read()

    if not conteudo:
        raise ValueError("O arquivo enviado esta vazio.")

    # =========================
    # ESCOLHA DO PARSER
    # =========================
    if extensao == "json":
        registros = _parse_json(conteudo)
    elif extensao == "csv":
        registros = _parse_csv(conteudo)
    elif extensao == "txt":
        registros = _parse_txt(conteudo)
    else:
        raise ValueError("Formato nao suportado. Use JSON, CSV ou TXT.")

    if not registros:
        raise ValueError("Nenhum registro valido foi encontrado no arquivo.")

    # Cria objetos Tarefa a partir dos registros
    tarefas = []
    for registro in registros:
        tarefas.append(
            Tarefa(
                titulo=registro["titulo"],
                descricao=registro["descricao"],
                data_entrega=registro["data_entrega"],
                prioridade=registro["prioridade"],
            )
        )

    # Insere todas as tarefas no banco de uma vez (mais eficiente)
    db.session.add_all(tarefas)
    db.session.commit()

    # Retorna quantidade de tarefas inseridas
    return len(tarefas)


# =========================
# DESFAZER ÚLTIMA AÇÃO
# =========================
def desfazer_ultima_acao():

    # Remove última ação da pilha
    ultima_acao = undo_stack.pop()

    if ultima_acao is None:
        return

    # Se a ação foi de criação, remove a tarefa do banco
    if ultima_acao["acao"] == "criar":
        tarefa = Tarefa.query.filter_by(
            titulo=ultima_acao["titulo"]
        ).first()

        if tarefa:
            db.session.delete(tarefa)
            db.session.commit()


# =========================
# NORMALIZAÇÃO DE DADOS
# =========================
def _normalizar_registro(registro):

    # Remove espaços e garante valores padrão
    titulo = (registro.get("titulo") or "").strip()
    descricao = (registro.get("descricao") or "Sem descricao").strip()
    data_entrega = (registro.get("data_entrega") or "").strip()
    prioridade = (registro.get("prioridade") or "Media").strip()

    # Validação mínima obrigatória
    if not titulo or not data_entrega:
        return None

    # Padroniza valores de prioridade
    if prioridade not in {"Alta", "Media", "Baixa", "Média"}:
        prioridade = "Media"

    if prioridade == "Média":
        prioridade = "Media"

    return {
        "titulo": titulo,
        "descricao": descricao,
        "data_entrega": data_entrega,
        "prioridade": prioridade,
    }


# =========================
# PARSER JSON
# =========================
def _parse_json(raw_bytes):

    try:
        payload = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("JSON invalido.") from exc

    # Aceita tanto objeto único quanto lista
    if isinstance(payload, dict):
        payload = [payload]

    if not isinstance(payload, list):
        raise ValueError("JSON deve conter um objeto ou uma lista de objetos.")

    registros_validos = []

    for item in payload:
        if isinstance(item, dict):
            registro = _normalizar_registro(item)
            if registro:
                registros_validos.append(registro)

    return registros_validos


# =========================
# PARSER CSV
# =========================
def _parse_csv(raw_bytes):

    try:
        texto = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV invalido (codificacao nao suportada).") from exc

    reader = csv.DictReader(io.StringIO(texto))

    registros_validos = []

    for linha in reader:
        registro = _normalizar_registro(linha)
        if registro:
            registros_validos.append(registro)

    return registros_validos


# =========================
# PARSER TXT
# =========================
def _parse_txt(raw_bytes):

    try:
        texto = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("TXT invalido (codificacao nao suportada).") from exc

    registros_validos = []

    # Cada linha representa uma tarefa separada por "|"
    for linha in texto.splitlines():

        linha = linha.strip()
        if not linha:
            continue

        partes = [parte.strip() for parte in linha.split("|")]

        registro = {
            "titulo": partes[0] if len(partes) > 0 else "",
            "descricao": partes[1] if len(partes) > 1 else "Sem descricao",
            "data_entrega": partes[2] if len(partes) > 2 else "",
            "prioridade": partes[3] if len(partes) > 3 else "Media",
        }

        registro_normalizado = _normalizar_registro(registro)

        if registro_normalizado:
            registros_validos.append(registro_normalizado)

    return registros_validos