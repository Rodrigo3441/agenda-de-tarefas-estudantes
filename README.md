# Agenda Academica

Aplicação web em Flask para gerenciar tarefas acadêmicas com apoio de estruturas de dados.
Inclui pilha para desfazer, fila de notificações e ordenação por data de entrega.

## Como executar

1. Crie e ative um ambiente virtual Python.
   -  (Windows) `venv\Scripts\activate` 
   -  (Linux/Mac) `source venv/bin/activate` 

2. Instale as dependências principais:
   - `pip install flask flask-sqlalchemy pymysql pytest`

3. Ajuste a conexão com banco em `src/app.py` (variavel `SQLALCHEMY_DATABASE_URI`) conforme seu MySQL local.

4. Execute a aplicação:
   - `python src/app.py`
   
5. Abra no navegador:
   - `http://127.0.0.1:5000`

## Importação de dados por arquivo

Na tela principal, use o botão de importacao para enviar arquivos `.json`, `.csv` ou `.txt`.
Exemplos prontos estão na pasta `data/`.

## Testes

Execute:

`python -m pytest -q`
