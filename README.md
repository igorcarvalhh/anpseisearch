# 📚 Biblioteca `anpseisearch`

Biblioteca Python para **consultas automatizadas de processos e documentos no SEI da ANP** (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis).
Permite buscar protocolos, documentos e processos usando filtros detalhados e retornar os resultados em formato organizado.

## 1️⃣ Pré-requisitos

Antes de usar a biblioteca, você precisa ter o Python instalado.

### a) Instalar Python

1. Acesse o site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Baixe a versão mais recente recomendada para o seu sistema operacional (Windows, macOS ou Linux).
3. Durante a instalação, **marque a opção "Add Python to PATH"**.
4. Finalize a instalação.

Para verificar se o Python está instalado, abra o terminal (Windows: `cmd`, macOS/Linux: `Terminal`) e digite:

```bash
python --version
```

Você deverá ver algo como:

```
Python 3.11.6
```

### b) Instalar pip

O pip geralmente já vem com o Python. Para verificar, digite:

```bash
pip --version
```

Deverá aparecer algo como:

```
pip 23.2.1 from ...
```

Se não estiver instalado, siga as instruções oficiais: [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)

## 2️⃣ Instalar a biblioteca `anpseisearch`

Você pode instalar de duas formas:

### a) Via PyPI (se estiver publicada)

```bash
pip install anpseisearch
```

### b) Instalando localmente (desenvolvimento ou versão não publicada)

1. Faça o download do código ou clone o repositório:

```bash
git clone https://github.com/seu-usuario/anpseisearch.git
cd anpseisearch
```

2. Instale a biblioteca no modo editável:

```bash
pip install -e .
```

Isso permite que alterações no código sejam refletidas automaticamente.

## 3️⃣ Estrutura do projeto

Após instalar, você verá arquivos importantes:

```
anpseisearch/
├─ __init__.py
├─ sei_register_searcher.py
├─ data/
│  ├─ process_ids.json
│  └─ document_ids.json
```

* **`sei_register_searcher.py`** → contém a lógica principal de pesquisa.
* **`data/process_ids.json`** → contém os tipos de processo válidos.
* **`data/document_ids.json`** → contém os tipos de documento válidos.

## 4️⃣ Como usar a biblioteca

### a) Importar e criar o pesquisador

```python
from anpseisearch import SeiRegisterSearcher

searcher = SeiRegisterSearcher()
```

### b) Definir filtros

Os filtros permitem refinar a pesquisa no SEI.
Somente as chaves listadas abaixo são aceitas:

| Filtro                         | Tipo | Descrição                                                                               |
| ------------------------------ | ---- | --------------------------------------------------------------------------------------- |
| `numero_protocolo_sei`         | str  | Número do protocolo do SEI (Processo ou Documento). Exemplo: `"5288361"`.               |
| `texto_pesquisa`               | str  | Palavras-chave para buscar no SEI.                                                      |
| `incluir_processos`            | bool | Incluir processos nos resultados. `True` → sim, `False` → não.                          |
| `incluir_documentos_gerados`   | bool | Incluir documentos gerados. `True` → sim, `False` → não.                                |
| `incluir_documentos_recebidos` | bool | Incluir documentos recebidos. `True` → sim, `False` → não.                              |
| `tipo_processo`                | str  | Tipo de processo, precisa estar listado em `process_ids.json`.                          |
| `tipo_documento`               | str  | Tipo de documento, precisa estar listado em `document_ids.json`.                        |
| `data_inicio`                  | str  | Data inicial no formato `YYYY-MM-DD`. Obrigatória para pesquisa por intervalo de tempo. |
| `data_fim`                     | str  | Data final no formato `YYYY-MM-DD`. Obrigatória para pesquisa por intervalo de tempo.   |

### c) Exemplo de definição de filtros

```python
filters = {
    "numero_protocolo_sei": "5288361",
    "texto_pesquisa": "Fiscalização",
    "incluir_processos": True,
    "incluir_documentos_gerados": False,
    "incluir_documentos_recebidos": False,
    "tipo_processo": "Aquisição de Bens e Serviços: Licitação",
    "tipo_documento": "Acordo de Cooperação Técnica",
    "data_inicio": "2025-09-05",
    "data_fim": "2025-09-07",
}

searcher.set_filters(filters)
```

### d) Executar pesquisa

```python
resultados = searcher.execute_search(page=0, rows_per_page=50)
```

* `page` → página da pesquisa (começa em 0).
* `rows_per_page` → quantidade de resultados por página.

O resultado é uma lista de dicionários:

```python
[
    {
        "protocolo": "1234567",
        "descricao": "Aquisição de equipamentos - Fiscalização",
        "unidade": "GAB/ANP",
        "data": "05/09/2025",
        "link": "https://sei.anp.gov.br/sei/controlador.php?...",
    },
    ...
]
```

## 5️⃣ Regras e restrições

* **Datas**: `data_inicio` e `data_fim` devem estar preenchidas.

* **Campos obrigatórios**: `txtDataInicio` e `txtDataFim`.

* **Campos `tipo_processo` e `tipo_documento`**:
  Devem ser iguais aos nomes listados nos arquivos `process_ids.json` e `document_ids.json`.
  Caso um valor inválido seja passado, o filtro será ignorado.

* **Campos booleanos (`incluir_processos`, etc.)**:
  Convertidos automaticamente para os valores aceitos pelo SEI:

  * `incluir_processos=True` → `"P"`
  * `incluir_documentos_gerados=True` → `"G"`
  * `incluir_documentos_recebidos=True` → `"R"`

* **`partialfields`**:
  Montado automaticamente com base nos filtros preenchidos. Somente os campos preenchidos são incluídos na query.

* **Página vazia**:
  Se a pesquisa não retornar resultados, a biblioteca retorna uma lista vazia `[]`.


## 6️⃣ Tratamento de erros

Caso a requisição falhe, a biblioteca lança uma exceção `SeiProcessSearchError`:

```python
from anpseisearch import SeiProcessSearchError

try:
    resultados = searcher.execute_search()
except SeiProcessSearchError as e:
    print("Erro na consulta:", e)
```

## 7️⃣ Exemplos avançados

* **Pesquisar apenas documentos gerados de um tipo específico:**

```python
filters = {
    "incluir_processos": False,
    "incluir_documentos_gerados": True,
    "tipo_documento": "Ofício",
    "data_inicio": "2025-01-01",
    "data_fim": "2025-12-31",
}

searcher.set_filters(filters)
resultados = searcher.execute_search()
```

* **Pesquisar por protocolo específico sem data** → **não permitido** (as datas são obrigatórias).

## 🔗 Links Úteis

* [SEI ANP](https://sei.anp.gov.br)
* [Documentação Python](https://docs.python.org/3/)
* [Instalação pip](https://pip.pypa.io/en/stable/installation/)

