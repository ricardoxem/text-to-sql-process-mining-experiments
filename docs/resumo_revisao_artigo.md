# Resumo do que foi preparado para a revisão do artigo

Este documento resume, de forma objetiva, o que foi organizado no repositório para apoiar a nova fase de revisão do artigo **Text-to-SQL in Process Mining: Revisiting Strategies and Expanding the Discussion**.

## 1. Direção adotada

A continuação do trabalho foi centralizada no repositório da revista:

```text
text-to-sql-process_mining
```

O repositório `text-2-sql` permanece apenas como referência histórica do artigo/base do arXiv e como fonte original do dataset e dos bancos SQLite.

## 2. Itens recuperados e centralizados

Foram reunidos no repositório da revista:

- dataset e arquivos gold em inglês e português;
- bancos SQLite em inglês e português;
- avaliador adaptado para EM e EX;
- pipeline próprio para execução de novos modelos;
- outputs brutos das novas execuções;
- arquivos de avaliação dos experimentos;
- resumo consolidado dos resultados.

## 3. Pipeline usado na nova fase

O pipeline da nova fase está em:

```text
journal_execution_pipeline/
```

Ele foi usado para rodar modelos locais via Ollama e modelos OpenAI via API, além de padronizar os resultados e executar as avaliações.

## 4. Experimentos executados

Foram executados experimentos com:

| Modelo | Cenário |
|---|---|
| Llama 3 8B | openAI-representation 0-shot |
| Llama 3.1 8B | openAI-representation 0-shot |
| Llama 3.1 8B | code-representation 5-shot |
| GPT-5.4 | code-representation 5-shot |

## 5. Principal resultado novo

O resultado mais importante foi obtido com **GPT-5.4** no cenário `code-representation 5-shot`.

| Idioma | EX | EM |
|---|---:|---:|
| Inglês | 71,60% | 57,04% |
| Português | 72,39% | 55,77% |

## 6. Comparação com o GPT-3.5 do artigo

| Idioma | Métrica | GPT-3.5 artigo | GPT-5.4 novo | Diferença |
|---|---:|---:|---:|---:|
| Inglês | EX | 57,16% | 71,60% | +14,44 p.p. |
| Português | EX | 56,25% | 72,39% | +16,14 p.p. |
| Inglês | EM | 61,33% | 57,04% | -4,29 p.p. |
| Português | EM | 58,37% | 55,77% | -2,60 p.p. |

## 7. Leitura para a revisão

A melhora em **Execution Accuracy (EX)** é o ponto mais forte dos novos experimentos. Essa métrica é especialmente relevante em Text-to-SQL porque avalia se a SQL gerada retorna o resultado correto no banco, mesmo quando a consulta não é textualmente idêntica à SQL gold.

A queda em **Exact Match (EM)** deve ser discutida com cuidado, pois pode ocorrer quando o modelo gera uma SQL diferente na forma, mas equivalente no resultado.

## 8. Arquivos principais no repositório

Documento detalhado da nova fase:

```text
docs/revisao_artigo_resultados.md
docs/revisao_artigo_resultados.html
```

Resumo dos resultados do pipeline:

```text
journal_execution_pipeline/RESULTS_SUMMARY.md
```

Artefatos brutos do GPT-5.4:

```text
journal_execution_pipeline/outputs/openai_en_code5_gpt54/
journal_execution_pipeline/outputs/openai_pt_code5_gpt54/
```

Avaliações do GPT-5.4:

```text
journal_execution_pipeline/evaluation_outputs/openai_en_code5_gpt54_EX/
journal_execution_pipeline/evaluation_outputs/openai_en_code5_gpt54_EM/
journal_execution_pipeline/evaluation_outputs/openai_pt_code5_gpt54_EX/
journal_execution_pipeline/evaluation_outputs/openai_pt_code5_gpt54_EM/
```

## 9. Próximos passos de escrita

Os próximos passos para a revisão do artigo são:

1. Inserir os resultados do GPT-5.4 nas tabelas do artigo.
2. Atualizar a discussão sobre desempenho dos modelos.
3. Explicar por que EX é a métrica mais relevante para a análise principal.
4. Decidir se serão executados outros modelos atualizados.
5. Preparar a resposta aos avaliadores com base nesses novos resultados.
