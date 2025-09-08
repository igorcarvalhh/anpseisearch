# 📚 anpseisearch

Biblioteca Python para **consulta automatizada de processos e documentos no SEI da ANP (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis)**.

Permite aplicar filtros avançados, realizar paginação e obter resultados estruturados em forma de lista de dicionários.

## 🚀 Instalação

```bash
pip install anpseisearch
```

Ou, se estiver desenvolvendo localmente:

```bash
git clone https://github.com/seu-repo/anpseisearch.git
cd anpseisearch
pip install -e .
```

## 🛠 Uso Básico

```python
from anpseisearch import SeiRegisterSearcher

# Criar instância do pesquisador
searcher = SeiRegisterSearcher()

# Definir filtros
filters = {
    "numero_protocolo_sei": "5288361",
    "texto_pesquisa": "Fiscalização",
    "incluir_processos": True,
    "incluir_documentos_gerados": False,
    "incluir_documentos_recebidos": False,
    "tipo_processo": "Aquisição de Bens e Serviços: Licitação",  # precisa ser um valor válido
    "tipo_documento": "Acordo de Cooperação Técnica",             # precisa ser um valor válido
    "data_inicio": "2025-09-05",
    "data_fim": "2025-09-07",
}

# Aplicar filtros
searcher.set_filters(filters)

# Executar pesquisa
resultados = searcher.execute_search(page=0, rows_per_page=50)

for r in resultados:
    print(r)
```

### 🔎 Exemplo de resultado retornado

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

## 🎛 Filtros Disponíveis

Ao usar `set_filters`, apenas as chaves abaixo são aceitas:

| Filtro                         | Tipo | Descrição                                                                               |
| ------------------------------ | ---- | --------------------------------------------------------------------------------------- |
| `numero_protocolo_sei`         | str  | Nº do protocolo do processo/documento no SEI. Exemplo: `"5288361"`.                     |
| `texto_pesquisa`               | str  | Texto livre a ser pesquisado.                                                           |
| `incluir_processos`            | bool | Incluir processos nos resultados (`True` → sim, `False` → não).                         |
| `incluir_documentos_gerados`   | bool | Incluir documentos gerados (`True` → sim, `False` → não).                               |
| `incluir_documentos_recebidos` | bool | Incluir documentos recebidos (`True` → sim, `False` → não).                             |
| `tipo_processo`                | str  | Tipo de processo. Deve ser um valor **pré-definido** em `process_ids.json`.             |
| `tipo_documento`               | str  | Tipo de documento. Deve ser um valor **pré-definido** em `document_ids.json`.           |
| `data_inicio`                  | str  | Data inicial no formato `YYYY-MM-DD`. Obrigatória para pesquisa por intervalo de tempo. |
| `data_fim`                     | str  | Data final no formato `YYYY-MM-DD`. Obrigatória para pesquisa por intervalo de tempo.   |


## ⚠️ Restrições e Regras de Uso

* **`tipo_processo` e `tipo_documento`**
  Não aceitam qualquer string.
  Os valores válidos estão nos arquivos:

  * `data/process_ids.json`
  * `data/document_ids.json`

  Esses arquivos contêm o **mapeamento entre nome e ID interno do SEI**.
  Por exemplo:

  `process_ids.json`

  ```json
  {
      "Aquisição de Bens e Serviços: Licitação": 123,
      "Contrato de Pesquisa": 456
  }
  ```

  `document_ids.json`

  ```json
  {
      "Acordo de Cooperação Técnica": 10,
      "Ofício": 20
  }
  ```

  Portanto:

  ```python
  filters = {
      "tipo_processo": "Aquisição de Bens e Serviços: Licitação",  # válido
      "tipo_documento": "Ofício",                                  # válido
  }
  ```

  Se um valor inexistente for passado, o campo ficará vazio e o filtro será ignorado.


## 📌 Tratamento de Erros

* Caso a requisição falhe, será lançada a exceção:

```python
from anpseisearch import SeiProcessSearchError

try:
    resultados = searcher.execute_search()
except SeiProcessSearchError as e:
    print("Erro na consulta:", e)
```

## 🧩 Estrutura Interna

* `DEFAULT_FORM_DATA` → parâmetros padrão exigidos pelo SEI.
* `FILTER_TO_SEI_MAP` → mapeia os nomes amigáveis de filtro para os nomes usados pelo SEI.
* `PROCESS_ID` e `DOCUMENT_ID` → carregados dinamicamente de arquivos JSON em `data/`.
* `_build_partialfields()` → monta dinamicamente a query `partialfields`.
* `execute_search()` → faz a requisição HTTP, trata erros e retorna os resultados parseados.
