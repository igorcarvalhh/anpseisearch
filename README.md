Perfeito! Aqui está uma versão **mais detalhada, clara e descritiva** do README, escrita para alguém que **não tem experiência com Python ou programação**, explicando cada passo de forma longa e estruturada:

---

# 📚 Biblioteca `anpseisearch`

A biblioteca **`anpseisearch`** foi desenvolvida para permitir consultas automatizadas de processos e documentos no **SEI da ANP** (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis). Ela permite que você busque protocolos, documentos e processos usando **filtros detalhados**, retornando os resultados de forma organizada em listas de registros com informações como protocolo, descrição, unidade, data e link direto para o processo/documento.

Esta biblioteca é especialmente útil para profissionais ou pesquisadores que precisam monitorar processos ou extrair dados do SEI de maneira rápida e automatizada, sem precisar acessar manualmente o sistema.

---

## 1️⃣ Pré-requisitos

Antes de começar a usar a biblioteca, é necessário **instalar o Python**, que é a linguagem de programação em que a biblioteca foi desenvolvida. Também precisaremos do **pip**, que é a ferramenta que permite instalar bibliotecas no Python.

### a) Instalar Python

1. Acesse o site oficial do Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Baixe a versão mais recente recomendada para o seu sistema operacional (Windows, macOS ou Linux).
3. Durante a instalação, **certifique-se de marcar a opção "Add Python to PATH"**, pois isso permitirá que você execute comandos do Python a partir do terminal ou prompt de comando.
4. Conclua a instalação seguindo as instruções da tela.

Para confirmar se o Python foi instalado corretamente, abra o terminal (no Windows, digite `cmd`; no macOS ou Linux, abra o Terminal) e execute:

```bash
python --version
```

Você deverá ver uma resposta semelhante a:

```
Python 3.11.6
```

Se você receber uma mensagem de erro, o Python não está corretamente instalado ou o PATH não foi configurado. Nesse caso, revise o passo 3 da instalação.

---

### b) Instalar pip

O **pip** normalmente é instalado junto com o Python. Para verificar se ele está disponível, execute no terminal:

```bash
pip --version
```

Você deverá ver algo semelhante a:

```
pip 23.2.1 from ...
```

Caso o pip não esteja instalado, siga as instruções oficiais para instalá-lo: [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)

O pip é necessário porque ele permite instalar a biblioteca `anpseisearch` e suas dependências automaticamente.

---

## 2️⃣ Instalar a biblioteca `anpseisearch`

A biblioteca pode ser instalada de duas formas:

### a) Instalando via PyPI (caso a biblioteca esteja publicada)

Se a biblioteca estiver disponível no repositório oficial do Python, você pode instalar com um único comando:

```bash
pip install anpseisearch
```

Esse comando fará o download da biblioteca e de todas as dependências necessárias.

### b) Instalando localmente (desenvolvimento ou versão não publicada)

Se você estiver usando a versão de desenvolvimento ou baixou o código diretamente do GitHub, siga estes passos:

1. Faça o download do código ou clone o repositório:

```bash
git clone https://github.com/seu-usuario/anpseisearch.git
cd anpseisearch
```

2. Instale a biblioteca no modo editável:

```bash
pip install -e .
```

O modo editável permite que você altere o código da biblioteca localmente e as alterações sejam refletidas imediatamente, sem precisar reinstalar a biblioteca.

---

## 3️⃣ Como usar a biblioteca

A biblioteca funciona em três etapas principais: **criar o objeto pesquisador**, **definir os filtros da pesquisa** e **executar a pesquisa**.

### a) Importar e criar o pesquisador

O primeiro passo é importar a classe `SeiRegisterSearcher` da biblioteca e criar uma instância do pesquisador:

```python
from anpseisearch import SeiRegisterSearcher

searcher = SeiRegisterSearcher()
```

A criação da instância inicializa todos os parâmetros internos da biblioteca, incluindo a configuração padrão de filtros e os arquivos de mapeamento de tipos de processo e documento.

---

### b) Definir filtros de pesquisa

A biblioteca permite refinar a pesquisa usando **filtros específicos**. Somente os filtros listados abaixo são aceitos:

| Filtro                         | Tipo | Descrição                                                                                              |
| ------------------------------ | ---- | ------------------------------------------------------------------------------------------------------ |
| `numero_protocolo_sei`         | str  | Número do protocolo do SEI (Processo ou Documento). Exemplo: `"5288361"`.                              |
| `texto_pesquisa`               | str  | Palavras-chave para buscar no SEI.                                                                     |
| `incluir_processos`            | bool | Incluir processos nos resultados. `True` → sim, `False` → não.                                         |
| `incluir_documentos_gerados`   | bool | Incluir documentos gerados. `True` → sim, `False` → não.                                               |
| `incluir_documentos_recebidos` | bool | Incluir documentos recebidos. `True` → sim, `False` → não.                                             |
| `tipo_processo`                | str  | Tipo de processo, deve ser exatamente igual a um dos valores listados no arquivo `process_ids.json`.   |
| `tipo_documento`               | str  | Tipo de documento, deve ser exatamente igual a um dos valores listados no arquivo `document_ids.json`. |
| `data_inicio`                  | str  | Data inicial do intervalo de pesquisa, no formato `YYYY-MM-DD`. Obrigatória.                           |
| `data_fim`                     | str  | Data final do intervalo de pesquisa, no formato `YYYY-MM-DD`. Obrigatória.                             |

Os filtros booleanos (`incluir_processos`, `incluir_documentos_gerados`, `incluir_documentos_recebidos`) são convertidos automaticamente para os valores aceitos pelo SEI:

* `True` → `"P"`, `"G"` ou `"R"` dependendo do campo
* `False` → vazio (não inclui o filtro na pesquisa)

Os filtros `tipo_processo` e `tipo_documento` precisam corresponder exatamente aos nomes cadastrados nos arquivos JSON de mapeamento (`process_ids.json` e `document_ids.json`). Caso contrário, o filtro será ignorado.

---

### c) Aplicar os filtros

Depois de definir os filtros desejados, aplique-os à instância do pesquisador:

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

A função `set_filters` atualiza os parâmetros internos da biblioteca e prepara os dados para a pesquisa, incluindo a montagem automática do campo `partialfields` que é usado para filtrar apenas os registros relevantes no SEI.

---

### d) Executar a pesquisa

Para realizar a pesquisa, use o método `execute_search`:

```python
resultados = searcher.execute_search(page=0, rows_per_page=50)
```

* `page` → número da página da pesquisa (começa em 0)
* `rows_per_page` → número de registros retornados por página

O resultado será uma lista de dicionários, cada um representando um protocolo ou documento encontrado. Cada dicionário contém:

* `"protocolo"` → número do protocolo
* `"descricao"` → descrição do processo/documento
* `"unidade"` → unidade responsável
* `"data"` → data do registro
* `"link"` → link direto para o protocolo no SEI

Exemplo de saída:

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

---

### e) Tratamento de erros

Caso a pesquisa falhe devido a problemas na requisição HTTP ou indisponibilidade do SEI, a biblioteca lançará uma exceção `SeiProcessSearchError`. É recomendável envolver a execução da pesquisa em um bloco `try/except`:

```python
from anpseisearch import SeiProcessSearchError

try:
    resultados = searcher.execute_search()
except SeiProcessSearchError as e:
    print("Erro na consulta:", e)
```

---

### f) Observações importantes

1. As datas (`data_inicio` e `data_fim`) são obrigatórias e devem estar no formato `YYYY-MM-DD`.
2. O campo `partialfields` é gerado automaticamente com base nos filtros preenchidos, e somente os filtros preenchidos são incluídos na query.
3. Se não houver resultados para a pesquisa, a biblioteca retorna uma lista vazia `[]`.
4. Valores incorretos para `tipo_processo` ou `tipo_documento` serão ignorados, portanto verifique os arquivos `process_ids.json` e `document_ids.json` antes de definir os filtros.

---

### 🔗 Links úteis

* [SEI ANP](https://sei.anp.gov.br)
* [Documentação oficial do Python](https://docs.python.org/3/)
* [Instalação do pip](https://pip.pypa.io/en/stable/installation/)

---

Se você quiser, posso criar **uma versão ainda mais didática**, com **passo a passo visual**, incluindo prints de terminal, exemplos de saída e instruções detalhadas de como alterar filtros, para **alguém que nunca usou Python** conseguir executar a biblioteca do zero.

Quer que eu faça isso?
