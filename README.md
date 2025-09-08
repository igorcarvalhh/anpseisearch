# anpseisearch

Ferramenta em Python para **extração de dados de processos e documentos no SEI da ANP (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis)**.

O pacote permite automatizar consultas públicas no sistema **SEI-ANP**, retornando informações como número do processo, unidade responsável, título, tipo de documento, link para o processo/documento e data de registro.

## 🚀 Instalação

```bash
pip install anpseisearch
```

## 📖 Exemplo de Uso

```python
from anpseisearch import SeiRegisterSearcher

# Cria a instância do buscador
searcher = SeiRegisterSearcher()

# Define filtros de pesquisa (form-data do SEI)
filters = {
    "txtDataInicio": "05/09/2025",
    "txtDataFim": "06/09/2025",
}
searcher.set_filters(filters=filters)

# Executa a busca
registers = searcher.execute_search()

# Itera sobre os registros encontrados
for reg in registers:
    print(reg)
```

## 🔎 Campos Disponíveis para Filtros

A consulta no SEI é baseada em um formulário HTML. Os principais campos que podem ser utilizados são:

| Campo                         | Descrição                             |
| ----------------------------- | ------------------------------------- |
| `txtProtocoloPesquisa`        | Número de protocolo                   |
| `chkSinProcessos`             | Filtrar somente processos (`P`)       |
| `txtParticipante`             | Participante                          |
| `txtUnidade`                  | Unidade responsável                   |
| `selTipoProcedimentoPesquisa` | Tipo de procedimento                  |
| `selSeriePesquisa`            | Série documental                      |
| `txtDataInicio`               | Data inicial da pesquisa (dd/mm/aaaa) |
| `txtDataFim`                  | Data final da pesquisa (dd/mm/aaaa)   |
| `txtNumeroDocumentoPesquisa`  | Número do documento                   |
| `txtAssinante`                | Assinante                             |
| `txtDescricaoPesquisa`        | Descrição do documento                |
| `txtAssunto`                  | Assunto                               |
| `txtSiglaUsuarioX`            | Sigla de usuários vinculados (1 a 4)  |


## 📊 Exemplo de Resultado Retornado

Cada registro retornado pela busca é estruturado como um dicionário contendo os seguintes campos:

| Campo                | Descrição                             |
| -------------------- | ------------------------------------- |
| `Título`             | Título completo do documento/processo |
| `Tipo do Documento`  | Ex.: Despacho de Instrução            |
| `Número Documento`   | Identificação do documento            |
| `Link do Documento`  | URL para visualização no SEI          |
| `Resumo Documento`   | Resumo textual                        |
| `Número do Processo` | Ex.: `48610.203905/2024-63`           |
| `Link Processo`      | URL do processo no SEI                |
| `Unidade`            | Unidade responsável                   |
| `Data`               | Data de registro                      |

📌 **Exemplo de saída**:

```json
{
  "Título": "Fiscalização: Instalações de Abastecimento, de Produção de Combustíveis e de Biocombustíveis nº48610.203905/2024-63 (Despacho de Instrução)",
  "Tipo do Documento": "Despacho de Instrução",
  "Número Documento": "5288361",
  "Link do Documento": "https://sei.anp.gov.br/sei/modulos/pesquisa/md_pesq_documento_consulta_externa.php?...",
  "Resumo Documento": "DESPACHO DE INSTRUÇÃO Processo nº 48610.203905/2024-63 In...",
  "Número do Processo": "48610.203905/2024-63",
  "Link Processo": "https://sei.anp.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?...",
  "Unidade": "SFI-CNPS-CJP DF",
  "Data": "06/09/2025"
}
```

## 📄 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
