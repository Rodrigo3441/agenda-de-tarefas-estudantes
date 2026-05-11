from database.db import db

# =========================
# MODELO DA ENTIDADE: TAREFA
# =========================
# Essa classe representa a tabela "tarefas" no banco de dados.
# Ela usa o SQLAlchemy (ORM), que permite trabalhar com o banco
# usando classes Python ao invés de SQL puro.

class Tarefa(db.Model):

    # Nome da tabela no banco de dados
    __tablename__ = "tarefas"

    # =========================
    # COLUNA: ID
    # =========================
    # Identificador único de cada tarefa
    # É chave primária (primary key) e auto-incremento
    id = db.Column(db.Integer, primary_key=True)

    # =========================
    # COLUNA: TÍTULO
    # =========================
    # Armazena o nome da tarefa
    # String com limite de 100 caracteres
    # Não pode ser vazio (nullable=False)
    titulo = db.Column(db.String(100), nullable=False)

    # =========================
    # COLUNA: DESCRIÇÃO
    # =========================
    # Armazena detalhes da tarefa
    # Tipo Text permite textos maiores
    # Campo obrigatório
    descricao = db.Column(db.Text, nullable=False)

    # =========================
    # COLUNA: DATA DE ENTREGA
    # =========================
    # Armazena a data limite da tarefa
    # Está como string para facilitar manipulação no sistema
    data_entrega = db.Column(db.String(20), nullable=False)

    # =========================
    # COLUNA: PRIORIDADE
    # =========================
    # Define o nível de importância da tarefa (ex: baixa, média, alta)
    prioridade = db.Column(db.String(20), nullable=False)