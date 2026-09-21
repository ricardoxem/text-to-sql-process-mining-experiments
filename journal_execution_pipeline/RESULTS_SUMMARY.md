# Journal Experiment Results Summary

Resumo dos experimentos executados para a continuidade do artigo "Text-to-SQL in Process Mining: Revisiting Strategies and Expanding the Discussion".

Data deste resumo: 2026-09-21.

## Contexto

O objetivo dos novos experimentos foi reproduzir o pipeline do artigo da revista e avaliar se modelos mais recentes melhoram os resultados, especialmente em Execution Accuracy (EX).

As metricas usadas sao:

- **EX (Execution Accuracy):** compara o resultado da execucao da SQL gerada contra o resultado da SQL gold no banco SQLite.
- **EM (Exact Match Accuracy):** compara a SQL gerada textualmente/estruturalmente com a SQL gold.

Para Text-to-SQL, EX tende a ser a metrica mais importante, pois consultas textualmente diferentes podem retornar o mesmo resultado correto.

## Resultados gerados localmente no pipeline

Estes resultados estao presentes em `journal_execution_pipeline/evaluation_outputs` nesta copia local do repositorio.

| Modelo | Cenario | Idioma | EX | EM |
|---|---|---:|---:|---:|
| Llama 3 8B via Ollama | openAI-representation 0-shot | Ingles | 36,37% | 32,27% |
| Llama 3 8B via Ollama | openAI-representation 0-shot | Portugues | 36,13% | 28,88% |
| Llama 3.1 8B via Ollama | openAI-representation 0-shot | Ingles | 39,15% | 35,29% |
| Llama 3.1 8B via Ollama | openAI-representation 0-shot | Portugues | 36,62% | 34,44% |
| Llama 3.1 8B via Ollama | code-representation 5-shot | Ingles | 52,51% | 49,55% |
| Llama 3.1 8B via Ollama | code-representation 5-shot | Portugues | 50,51% | 47,67% |

## Resultados GPT-5.4 executados na maquina do laboratorio

O experimento com GPT-5.4 foi executado na maquina do laboratorio em:

```text
/mnt/dados/home/rscheicher/repositories/text-to-sql-process-mining-experiments
```

Os resultados finais calculados foram:

| Modelo | Cenario | Idioma | EX | EM |
|---|---|---:|---:|---:|
| GPT-5.4 | code-representation 5-shot | Ingles | 71,60% | 57,04% |
| GPT-5.4 | code-representation 5-shot | Portugues | 72,39% | 55,77% |

Artefatos versionados no repositorio:

```text
journal_execution_pipeline/outputs/openai_en_code5_gpt54/RESULTS_MODEL-gpt-5.4.txt
journal_execution_pipeline/outputs/openai_en_code5_gpt54/responses.jsonl
journal_execution_pipeline/outputs/openai_en_code5_gpt54/run_metadata.json
journal_execution_pipeline/outputs/openai_pt_code5_gpt54/RESULTS_MODEL-gpt-5.4.txt
journal_execution_pipeline/outputs/openai_pt_code5_gpt54/responses.jsonl
journal_execution_pipeline/outputs/openai_pt_code5_gpt54/run_metadata.json
journal_execution_pipeline/evaluation_outputs/openai_en_code5_gpt54_EX/score.tsv
journal_execution_pipeline/evaluation_outputs/openai_en_code5_gpt54_EM/score.tsv
journal_execution_pipeline/evaluation_outputs/openai_pt_code5_gpt54_EX/score.tsv
journal_execution_pipeline/evaluation_outputs/openai_pt_code5_gpt54_EM/score.tsv
```

Os artefatos brutos do GPT-5.4 foram recuperados da maquina do laboratorio, copiados para este repositorio e versionados no commit `870fc2e` (`Add GPT-5.4 experiment outputs`).

## Custo do experimento GPT-5.4

| Idioma | Input tokens | Output tokens | Reasoning tokens | Custo estimado |
|---|---:|---:|---:|---:|
| Ingles | 663.980 | 55.007 | 0 | US$ 2,49 |
| Portugues | 725.975 | 56.251 | 0 | US$ 2,66 |
| Total | 1.389.955 | 111.258 | 0 | US$ 5,14 |

## Comparacao com o melhor GPT do artigo

Melhor referencia anotada do artigo: GPT-3.5 no cenario code-representation 5-shot.

| Idioma | Metrica | GPT-3.5 artigo | GPT-5.4 novo | Diferenca |
|---|---:|---:|---:|---:|
| Ingles | EX | 57,16% | 71,60% | +14,44 p.p. |
| Portugues | EX | 56,25% | 72,39% | +16,14 p.p. |
| Ingles | EM | 61,33% | 57,04% | -4,29 p.p. |
| Portugues | EM | 58,37% | 55,77% | -2,60 p.p. |

## Leitura inicial

O GPT-5.4 apresentou ganho expressivo em Execution Accuracy nos dois idiomas. A queda em EM nao invalida o resultado, pois o modelo pode gerar SQLs diferentes da SQL gold, mas semanticamente corretas e com o mesmo resultado de execucao.

Para a revisao do artigo, o ponto mais forte e reportar o aumento em EX, pois ele indica melhora pratica na capacidade de gerar consultas que retornam a resposta correta no banco.

## Proximos passos recomendados

1. Criar um documento em portugues descrevendo a nova fase de experimentos para a revisao do artigo.
2. Gerar versoes equivalentes em Markdown e HTML para facilitar leitura e compartilhamento.
3. Conferir se os resultados precisam ser reformatados para as tabelas do artigo.
4. Decidir com a professora Sara e a Thais se novas rodadas devem incluir outros modelos ou apenas GPT-5.4 como atualizacao principal.
