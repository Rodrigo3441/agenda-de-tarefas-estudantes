# Agenda Acadêmica

Sistema web desenvolvido em Python com Flask para gerenciamento de tarefas acadêmicas.

O projeto utiliza estruturas de dados e algoritmos clássicos para organizar informações:
- Pilha para funcionalidade de desfazer ações;
- Fila para gerenciamento de notificações;
- Merge Sort e Insertion Sort para ordenação de tarefas por data de entrega.

Os dados são persistidos em banco de dados MySQL utilizando SQLAlchemy.

## Funcionalidades

- Cadastro, edição e exclusão de tarefas acadêmicas
- Ordenação de tarefas por data utilizando Merge Sort e Insertion Sort
- Sistema de desfazer ações com Pilha (LIFO)
- Gerenciamento de notificações com Fila (FIFO)
- Importação de tarefas via arquivos `.json`, `.csv` e `.txt`
- Persistência de dados com MySQL + SQLAlchemy
- Interface web desenvolvida com Flask
- Testes automatizados com Pytest

## Tecnologias Utilizadas

- Python 3
- Flask
- Jinja2
- SQLAlchemy
- MySQL
- PyMySQL
- HTML5
- CSS3
- Pytest

## Estruturas de Dados e Algoritmos

- Pilha (LIFO) para funcionalidade de desfazer ações
- Fila (FIFO) para gerenciamento de notificações
- Insertion Sort para ordenação de listas menores
- Merge Sort para ordenação eficiente de grandes listas de tarefas

## Estrutura de Diretórios

```text
/
├── src/
│   ├── core/
│   │   ├── undo_stack.py
│   │   ├── fila_notificacao.py
│   │   └── ordenacao.py
│   │
│   ├── service/
│   │   └── tarefa_service.py
│   │
│   ├── database/
│   │   └── models.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── resultado.html
│   │   └── editar.html
│   │
│   ├── static/
│   │   └── css/
│   │
│   └── app.py
│
├── tests/
├── data/
├── doc/
├── README.md
└── .gitignore
```



## Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/Rodrigo3441/agenda-de-tarefas-estudantes
```

### 2. Crie e ative o ambiente virtual

#### Windows
```bash
venv\Scripts\activate
```

#### Linux/Mac
```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Ajuste a variável `SQLALCHEMY_DATABASE_URI` no arquivo `src/app.py` conforme sua configuração local do MySQL.

Exemplo:

```python
mysql+pymysql://usuario:senha@localhost/agenda_db
```

### 5. Execute a aplicação

```bash
python src/app.py
```

### 6. Acesse no navegador

```text
http://127.0.0.1:5000
```

## Importação de Dados

O sistema permite importar tarefas acadêmicas por arquivos nos formatos:

- `.json`
- `.csv`
- `.txt`

Na tela principal, utilize o botão de importação para enviar o arquivo desejado.

Exemplos de arquivos para teste estão disponíveis na pasta `data/`.

## Testes

Os testes automatizados foram desenvolvidos utilizando Pytest para validar as principais operações das estruturas de dados implementadas no projeto.

Para executar os testes:

```bash
python -m pytest -q
```

## Interface

### Tela Principal

![Tela principal](docs/images/main_screen.jpeg)

## Licença

Este projeto está licenciado sob a licença MIT.
