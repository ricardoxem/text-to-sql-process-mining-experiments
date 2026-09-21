# Nova fase de experimentos para revisão do artigo

## 1. Objetivo

Este documento resume a nova fase de experimentos realizada para apoiar a revisão do artigo **Text-to-SQL in Process Mining: Revisiting Strategies and Expanding the Discussion**.

A principal motivação foi verificar se a execução do mesmo cenário experimental com modelos mais recentes poderia melhorar os resultados apresentados originalmente, especialmente na métrica **Execution Accuracy (EX)**.

## 2. Contexto dos repositórios

Durante a retomada do trabalho, foram analisados dois repositórios principais:

| Repositório | Papel no trabalho |
|---|---|
| `text-2-sql` | Repositório associado ao artigo/base do arXiv, usado como referência histórica e fonte do dataset, dos arquivos gold e dos bancos SQLite. |
| `text-to-sql-process_mining` | Repositório associado ao artigo da revista. Passou a ser o repositório central para a continuação do trabalho, reprodução dos experimentos e armazenamento dos novos resultados. |

A partir dessa avaliação, decidiu-se concentrar a nova fase no repositório `text-to-sql-process_mining`, mantendo o `text-2-sql` apenas como referência do dataset/base original.

## 3. O que foi recuperado e organizado

Foram recuperados e centralizados no repositório da revista:

- os bancos SQLite em inglês e português;
- os arquivos gold em inglês e português;
- o avaliador adaptado usado para calcular EM e EX;
- os scripts do novo pipeline de execução;
- os outputs brutos dos experimentos novos;
- os arquivos de avaliação com os scores obtidos.

Os resultados mais recentes estão concentrados em:

```text
journal_execution_pipeline/
```

## 4. Pipeline criado para os novos experimentos

Foi criado um pipeline separado do código original para facilitar reprodução e novas rodadas experimentais:

```text
journal_execution_pipeline/
  configs/
  src/
  outputs/
  evaluation_outputs/
  evaluation_tools/
  RESULTS_SUMMARY.md
```

Esse pipeline permite:

- executar modelos via OpenAI;
- executar modelos locais via Ollama;
- preparar saídas no formato esperado pelo avaliador;
- calcular Exact Match Accuracy (EM);
- calcular Execution Accuracy (EX);
- registrar metadados de execução e custo.

## 5. Dados e avaliação

A avaliação usa o dataset Text-to-SQL no domínio de Process Mining, com versões em inglês e português.

As métricas utilizadas foram:

| Métrica | Descrição |
|---|---|
| EM | Exact Match Accuracy. Mede a correspondência textual/estrutural entre a SQL gerada e a SQL gold. |
| EX | Execution Accuracy. Mede se a SQL gerada retorna o mesmo resultado que a SQL gold quando executada no banco SQLite. |

Para Text-to-SQL, a métrica EX tende a ser mais representativa, pois duas consultas SQL podem ser diferentes na forma textual e ainda assim produzir o mesmo resultado correto.

## 6. Modelos executados nesta nova fase

Foram executados novos experimentos com modelos locais e com modelo OpenAI atualizado:

| Modelo | Execução | Cenário |
|---|---|---|
| Llama 3 8B | Ollama | openAI-representation 0-shot |
| Llama 3.1 8B | Ollama | openAI-representation 0-shot |
| Llama 3.1 8B | Ollama | code-representation 5-shot |
| GPT-5.4 | OpenAI API | code-representation 5-shot |

O experimento com GPT-5.4 foi executado na máquina do laboratório disponibilizada pela professora Sara e depois os artefatos foram copiados para este repositório.

## 7. Resultados obtidos

### 7.1 Resultados com Llama/Ollama

| Modelo | Cenário | Idioma | EX | EM |
|---|---|---:|---:|---:|
| Llama 3 8B | openAI-representation 0-shot | Inglês | 36,37% | 32,27% |
| Llama 3 8B | openAI-representation 0-shot | Português | 36,13% | 28,88% |
| Llama 3.1 8B | openAI-representation 0-shot | Inglês | 39,15% | 35,29% |
| Llama 3.1 8B | openAI-representation 0-shot | Português | 36,62% | 34,44% |
| Llama 3.1 8B | code-representation 5-shot | Inglês | 52,51% | 49,55% |
| Llama 3.1 8B | code-representation 5-shot | Português | 50,51% | 47,67% |

### 7.2 Resultados com GPT-5.4

| Modelo | Cenário | Idioma | EX | EM |
|---|---|---:|---:|---:|
| GPT-5.4 | code-representation 5-shot | Inglês | 71,60% | 57,04% |
| GPT-5.4 | code-representation 5-shot | Português | 72,39% | 55,77% |

## 8. Comparação com o melhor resultado GPT reportado no artigo

A melhor referência anotada do artigo para GPT foi o GPT-3.5 no cenário `code-representation 5-shot`.

| Idioma | Métrica | GPT-3.5 artigo | GPT-5.4 novo | Diferença |
|---|---:|---:|---:|---:|
| Inglês | EX | 57,16% | 71,60% | +14,44 p.p. |
| Português | EX | 56,25% | 72,39% | +16,14 p.p. |
| Inglês | EM | 61,33% | 57,04% | -4,29 p.p. |
| Português | EM | 58,37% | 55,77% | -2,60 p.p. |

## 9. Interpretação inicial

O resultado mais relevante desta nova fase é o aumento expressivo em **Execution Accuracy** com GPT-5.4 nos dois idiomas.

A queda em EM não necessariamente indica piora prática, pois o modelo pode gerar consultas SQL diferentes da SQL gold, mas que retornam o mesmo resultado ao serem executadas. Por isso, para a discussão do artigo, o principal ponto positivo é a melhora em EX.

Esses resultados sugerem que apenas atualizar o modelo, mantendo o mesmo cenário experimental, já pode gerar melhora relevante na capacidade de produzir SQLs semanticamente corretas.

## 10. Custo do experimento GPT-5.4

| Idioma | Input tokens | Output tokens | Reasoning tokens | Custo estimado |
|---|---:|---:|---:|---:|
| Inglês | 663.980 | 55.007 | 0 | US$ 2,49 |
| Português | 725.975 | 56.251 | 0 | US$ 2,66 |
| Total | 1.389.955 | 111.258 | 0 | US$ 5,14 |

## 11. Arquivos versionados no repositório

Os principais artefatos da nova execução estão em:

```text
journal_execution_pipeline/outputs/openai_en_code5_gpt54/
journal_execution_pipeline/outputs/openai_pt_code5_gpt54/
journal_execution_pipeline/evaluation_outputs/openai_en_code5_gpt54_EX/
journal_execution_pipeline/evaluation_outputs/openai_en_code5_gpt54_EM/
journal_execution_pipeline/evaluation_outputs/openai_pt_code5_gpt54_EX/
journal_execution_pipeline/evaluation_outputs/openai_pt_code5_gpt54_EM/
```

O commit com os artefatos brutos do GPT-5.4 é:

```text
870fc2e Add GPT-5.4 experiment outputs
```

## 12. Relação com os pareceres

O resumo dos pareceres dos revisores e dos encaminhamentos sugeridos para a revisão do artigo está em:

```text
docs/revisao_pareceres.md
docs/revisao_pareceres.html
```

## 13. Próximos passos

Os próximos passos sugeridos para a revisão do artigo são:

1. Revisar as tabelas do artigo para incluir os resultados com GPT-5.4.
2. Discutir a diferença entre EM e EX, destacando a importância de EX para Text-to-SQL.
3. Avaliar se será necessário rodar outros modelos atualizados ou se GPT-5.4 será suficiente como evidência principal.
4. Organizar a resposta aos avaliadores conectando os novos resultados com os pontos levantados na revisão.
5. Validar com a professora Sara e a Thaís quais resultados entrarão na nova versão do artigo.
