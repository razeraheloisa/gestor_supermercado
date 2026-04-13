# gestor_supermercado
Repósitorio para o gestor de supermercado
# 🛒 Gestor de Supermercado

Sistema de gestão de supermercado em Python com interface de terminal, que permite gerir **categorias** e **produtos** através de um menu interativo com operações CRUD completas.

---

## 📋 Índice

- [Descrição](#descrição)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
- [Utilização](#utilização)
- [Validações e Erros](#validações-e-erros)
- [Estrutura de Dados](#estrutura-de-dados)

---

## Descrição

O **Gestor de Supermercado** é uma aplicação de linha de comandos desenvolvida em Python que permite gerir um catálogo de produtos organizados por categorias. Os dados são armazenados em memória (dicionários Python) durante a execução do programa.

O projeto foi desenvolvido **sem utilização de classes**, recorrendo apenas a funções e dicionários, seguindo uma arquitetura modular distribuída por vários ficheiros.

---

## Estrutura do Projeto

```
gestor-supermercado/
│
├── main.py          # Ponto de entrada; menus e navegação terminal
├── categoria.py     # CRUD de categorias
├── produto.py       # CRUD de produtos
├── utils.py         # Funções auxiliares (geração de IDs e validações)
└── README.md
```

### Descrição dos Ficheiros

| Ficheiro | Responsabilidade |
|---|---|
| `main.py` | Menu principal, submenus e interação com o utilizador |
| `categoria.py` | Lógica de negócio e armazenamento das categorias |
| `produto.py` | Lógica de negócio e armazenamento dos produtos |
| `utils.py` | Geração de IDs automáticos e validação de inputs |

---

## Funcionalidades

### Categorias
- **Criar** categoria com nome e descrição
- **Listar** todas as categorias
- **Consultar** categoria por ID
- **Atualizar** nome e/ou descrição de uma categoria
- **Remover** categoria (bloqueado se existirem produtos associados)

### Produtos
- **Criar** produto com nome, preço, quantidade em stock, categoria e peso
- **Listar** todos os produtos
- **Listar** produtos filtrados por categoria
- **Consultar** produto por ID
- **Atualizar** qualquer campo de um produto
- **Remover** produto

---

## Pré-requisitos

- Python **3.6** ou superior
- Sem dependências externas — utiliza apenas a biblioteca padrão do Python

---

## Como Executar

1. Clone ou descarregue o repositório para a sua máquina local.

2. Na pasta do projeto, execute:

```bash
python main.py
```

---

## Utilização

Ao iniciar o programa, é apresentado o menu principal:

```
╔══════════════════════════════╗
║    GESTOR DE SUPERMERCADO    ║
╠══════════════════════════════╣
║  1 - Gerir Categorias        ║
║  2 - Gerir Produtos          ║
║  0 - Sair                    ║
╚══════════════════════════════╝
```

### Exemplo de fluxo

**1. Criar uma categoria:**
```
===== MENU CATEGORIAS =====
Escolha uma opção: 1
Nome da categoria: Frutas
Descrição: Frutas frescas e da época
[201] Categoria criada com sucesso. ID: C001
```

**2. Criar um produto nessa categoria:**
```
===== MENU PRODUTOS =====
Escolha uma opção: 1
Nome do produto: Maçã
Preço (ex: 1.99): 0.99
Quantidade em stock: 150
ID da categoria: C001
Peso em kg (ex: 0.500): 0.200
[201] Produto criado com sucesso. ID: P001
```

**3. Listar todos os produtos:**
```
ID       Nome                   Preço (€)  Stock      Peso (kg)  Categoria
---------------------------------------------------------------------------
P001     Maçã                   0.99       150        0.200      Frutas
```

### IDs Automáticos

Os IDs são gerados automaticamente com o seguinte formato:

| Entidade  | Formato | Exemplo |
|-----------|---------|---------|
| Categoria | `C` + 3 dígitos | `C001`, `C002` |
| Produto   | `P` + 3 dígitos | `P001`, `P002` |

> Os IDs são inseridos automaticamente — o utilizador não os define manualmente.

---

## Validações e Erros

O sistema utiliza códigos de estado HTTP para comunicar o resultado de cada operação:

| Código | Significado | Exemplo |
|--------|-------------|---------|
| `201`  | Criação bem-sucedida | Categoria ou produto criado |
| `200`  | Atualização/remoção bem-sucedida | Dados atualizados ou removidos |
| `400`  | Dados inválidos | Preço negativo, campo vazio |
| `404`  | Não encontrado | ID de produto ou categoria inexistente |
| `409`  | Conflito | Nome de categoria duplicado; remoção de categoria com produtos |

### Regras de validação

- **Nome** — não pode estar vazio
- **Preço** — número decimal não negativo (ex: `1.99`)
- **Quantidade** — número inteiro não negativo (ex: `10`)
- **Peso** — número decimal positivo (ex: `0.500`)
- **Categoria** — tem de existir no sistema antes de ser associada a um produto
- **Nome de categoria** — não pode ser duplicado (insensível a maiúsculas/minúsculas)

---

## Estrutura de Dados

Os dados são guardados em dicionários globais durante a execução do programa. Ao terminar o programa, os dados não são persistidos.

### Categoria

```python
categorias = {
    "C001": {
        "nome_categoria": "Frutas",
        "descricao": "Frutas frescas e da época"
    }
}
```

### Produto

```python
produtos = {
    "P001": {
        "nome": "Maçã",
        "preco": 0.99,
        "quantidade_stock": 150,
        "id_categoria": "C001",
        "peso": 0.200
    }
}
```

---

> **Nota:** Os dados são armazenados apenas em memória. Ao encerrar o programa, toda a informação é perdida. Para persistência, seria necessário integrar uma base de dados ou exportação para ficheiro.
