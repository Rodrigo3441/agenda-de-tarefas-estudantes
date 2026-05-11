from flask_sqlalchemy import SQLAlchemy

# =========================
# CONFIGURAÇÃO DO BANCO DE DADOS
# =========================
# Aqui estamos importando o SQLAlchemy, que é uma ferramenta ORM
# (Object Relational Mapper), usada para facilitar a comunicação
# entre o Python e o banco de dados.

# Em vez de escrever SQL puro, usamos objetos Python para manipular tabelas.

# =========================
# INSTÂNCIA DO BANCO
# =========================
# Criamos a instância do banco de dados que será usada em toda a aplicação.
# Essa instância será inicializada dentro do Flask posteriormente.

db = SQLAlchemy()