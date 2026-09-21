# Resumo dos pareceres e encaminhamentos para a revisão do artigo

Este documento resume os principais pontos levantados pelos revisores no arquivo `papers/revisoes.txt` e organiza possíveis encaminhamentos para a nova fase de revisão do artigo **Text-to-SQL in Process Mining: Revisiting Strategies and Expanding the Discussion**.

## 1. Visão geral dos pareceres

Os pareceres foram positivos quanto à originalidade, à organização metodológica e à contribuição do benchmark bilíngue para Text-to-SQL no domínio de Process Mining. A recomendação geral foi de **Major Revision**, com foco em ampliar a força experimental, melhorar a discussão qualitativa e reforçar a reprodutibilidade.


## 2. Resumo de cada parecer

### 2.1 Reviewer 1

O Reviewer 1 avaliou o artigo como uma contribuição relevante e original, com desenho experimental claro, uso adequado das métricas EM e EX, análise por complexidade SQL e foco em um domínio ainda pouco explorado em Text-to-SQL: Process Mining. Também destacou positivamente a criação do benchmark bilíngue `text2SQL4PM`, a avaliação cross-lingual e o uso de diferentes estratégias de prompt.

As principais críticas foram que os modelos avaliados não eram os mais recentes, o que reduzia a conexão com o estado da arte; que a análise qualitativa de erros ainda era limitada; e que o foco em SQL, embora justificável, poderia ser melhor conectado às práticas reais de Process Mining, especialmente ao uso de PQL. O parecer também apontou impacto prático ainda pouco desenvolvido, resultados originais modestos, problemas de legibilidade em algumas figuras, pequenos erros tipográficos e necessidade de detalhar melhor trabalhos futuros.

A recomendação geral do Reviewer 1 foi **Major Revision**, com nota geral **3,8/5**. A direção sugerida foi fortalecer o artigo por meio de modelos mais atuais, análise qualitativa mais profunda, melhor discussão de impacto prático e ajustes de apresentação.

### 2.2 Reviewer 2

O Reviewer 2 considerou o manuscrito claro, bem estruturado e relevante para a avaliação de modelos de linguagem em Text-to-SQL no contexto de Process Mining. Destacou como pontos fortes a comparação entre estilos de prompt, o uso de diferentes quantidades de exemplos in-context e as análises por complexidade SQL e categorias de template, que ajudam a diagnosticar onde os modelos acertam ou falham.

As sugestões de melhoria foram mais específicas e metodológicas. O revisor pediu maior clareza sobre como os exemplos few-shot são selecionados, incluindo conjunto candidato, exclusões e controle de intenções duplicadas ou muito próximas. Também solicitou a inclusão dos parâmetros de geração dos modelos, como temperature, top-p, max tokens, retries e stopping rules. Outro ponto importante foi a sugestão de reportar quantas queries gold retornam resultado vazio, pois isso pode tornar a Execution Accuracy otimista. Além disso, recomendou expandir os trabalhos relacionados sobre estratégias modernas de prompting para Text-to-SQL e corrigir inconsistências textuais, como o typo `Mediun class` e o uso de `event` versus `activity`.

Em resumo, o Reviewer 2 não questionou a relevância geral do trabalho, mas pediu ajustes que melhoram reprodutibilidade, clareza metodológica e robustez da avaliação.

## 3. Pontos fortes destacados

Os revisores destacaram os seguintes aspectos positivos:

- desenho experimental claro e sistemático;
- uso combinado das métricas EM e EX;
- análise por complexidade SQL e por templates;
- foco original em Process Mining, um domínio ainda pouco explorado em Text-to-SQL;
- criação e uso do benchmark bilíngue `text2SQL4PM`;
- comparação entre diferentes estratégias de prompt e números de exemplos in-context;
- disponibilidade de dataset, código e metodologia, favorecendo reprodutibilidade;
- discussão equilibrada das limitações.

## 4. Principais críticas e sugestões

As críticas e sugestões podem ser agrupadas nos seguintes temas.

### 4.1 Atualização dos modelos avaliados

Um dos pontos centrais foi que os modelos avaliados originalmente não representavam mais o estado da arte, pois não incluíam modelos mais recentes, como GPT-4 ou alternativas equivalentes.

Esse ponto está diretamente relacionado aos novos experimentos executados nesta fase, especialmente com GPT-5.4.

### 4.2 Resultados modestos

O Reviewer 1 apontou que os melhores resultados originais, aproximadamente 48% em EM e 57% em EX, limitavam a aplicabilidade prática imediata.

A nova rodada com GPT-5.4 responde parcialmente a essa crítica, pois elevou a Execution Accuracy para:

| Idioma | EX com GPT-5.4 |
|---|---:|
| Inglês | 71,60% |
| Português | 72,39% |

### 4.3 Análise qualitativa de erros

Foi apontado que o artigo menciona erros e interpretações incorretas, mas não aprofunda tipologias de erro nem apresenta exemplos suficientes.

Esse ponto ainda precisa ser trabalhado na revisão do manuscrito.

### 4.4 Explicação da seleção few-shot

O Reviewer 2 solicitou maior clareza sobre a seleção dos exemplos few-shot, incluindo:

- qual é o conjunto candidato;
- o que é excluído;
- como são evitadas intenções duplicadas ou muito próximas;
- como a remoção de paráfrases é feita.

Esse ponto deve ser respondido metodologicamente no texto do artigo.

### 4.5 Parâmetros de geração dos modelos

Foi solicitada a inclusão dos principais parâmetros de geração, como:

- temperature;
- top-p;
- max tokens;
- retries;
- stopping rules.

Essa sugestão está ligada à reprodutibilidade. Para os novos experimentos, os metadados e configurações foram versionados no repositório.

### 4.6 Execution Accuracy com resultados vazios

O Reviewer 2 observou que a métrica EX pode parecer otimista quando a query gold retorna resultado vazio.

Foi sugerido reportar a frequência de gold queries com resultado vazio:

- no total;
- por classe de complexidade.

Esse ponto ainda precisa de análise adicional no pipeline.

### 4.7 Trabalhos relacionados e estratégias de prompting

Foi sugerido expandir a seção de trabalhos relacionados para contextualizar melhor estratégias modernas de prompting em Text-to-SQL, como:

- decomposition prompting;
- schema filtering;
- candidate column selection;
- self-correction;
- refinement leve.

### 4.8 Alinhamento com Process Mining e PQL

O Reviewer 1 observou que o foco em SQL é justificável, mas reduz a conexão direta com práticas usuais de Process Mining, que frequentemente usam PQL ou ferramentas específicas da área.

A revisão deve reforçar melhor essa escolha e indicar caminhos futuros mais concretos para PQL.

### 4.9 Aplicabilidade prática e impacto industrial

Foi apontado que o artigo poderia discutir melhor cenários de adoção prática, como integração com ferramentas de BI, BPM ou Process Mining.

Esse ponto deve ser tratado na introdução, discussão ou seção de implicações práticas.

### 4.10 Melhorias de apresentação

Foram mencionados problemas menores de apresentação:

- figuras com fontes/legendas pequenas;
- typo `Mediun class`, que deve ser corrigido para `Medium class`;
- inconsistência terminológica, especialmente entre `event` e `activity`.

## 5. Relação entre os pareceres e o que já foi feito

| Ponto dos revisores | O que já foi feito | Situação |
|---|---|---|
| Modelos avaliados não são os mais atuais | Foram executados novos experimentos com GPT-5.4 e Llama 3.1 | Parcialmente respondido |
| Resultados originais modestos | GPT-5.4 elevou EX para 71,60% em inglês e 72,39% em português | Respondido com novos resultados |
| Reprodutibilidade | Pipeline, outputs, scores e metadados foram versionados | Avanço importante |
| Parâmetros de geração | Configurações e metadados dos novos experimentos foram salvos | Precisa ser descrito no artigo |
| Seleção few-shot pouco clara | O cenário code-representation 5-shot foi reproduzido no pipeline | Precisa explicação textual detalhada |
| EX com gold vazio | Ainda não analisado | Pendente |
| Análise qualitativa de erros | Ainda não aprofundada | Pendente |
| Trabalhos relacionados sobre prompting | Ainda não revisado no manuscrito | Pendente |
| Discussão sobre PQL | Ainda precisa ser fortalecida | Pendente |
| Aplicabilidade prática | Ainda precisa ser expandida | Pendente |
| Figuras, typos e terminologia | Ainda precisa revisão textual | Pendente |

## 6. Resultados novos mais relevantes para a resposta aos revisores

Os novos resultados com GPT-5.4 são o principal elemento experimental para responder às críticas sobre modelos desatualizados e desempenho limitado.

| Idioma | Métrica | GPT-3.5 artigo | GPT-5.4 novo | Diferença |
|---|---:|---:|---:|---:|
| Inglês | EX | 57,16% | 71,60% | +14,44 p.p. |
| Português | EX | 56,25% | 72,39% | +16,14 p.p. |
| Inglês | EM | 61,33% | 57,04% | -4,29 p.p. |
| Português | EM | 58,37% | 55,77% | -2,60 p.p. |

A interpretação inicial é que o modelo mais recente melhora substancialmente a capacidade de gerar SQLs que retornam o resultado correto, mesmo que nem sempre reproduza exatamente a mesma forma textual da SQL gold.

## 7. Próximas ações sugeridas

Para avançar na revisão do artigo, recomenda-se:

1. Incorporar os resultados do GPT-5.4 nas tabelas principais do artigo.
2. Adicionar uma discussão explícita sobre a diferença entre EM e EX.
3. Explicar melhor a seleção de exemplos few-shot.
4. Documentar parâmetros de geração dos modelos.
5. Implementar ou calcular a análise de gold queries com resultado vazio.
6. Criar uma análise qualitativa de erros com exemplos representativos.
7. Expandir trabalhos relacionados sobre estratégias modernas de prompting para Text-to-SQL.
8. Reforçar a discussão sobre SQL, PQL e aplicabilidade em Process Mining.
9. Revisar figuras, typos e terminologia antes da nova submissão.

## 8. Documentos relacionados

A documentação detalhada dos novos experimentos está em:

```text
docs/revisao_artigo_resultados.md
docs/revisao_artigo_resultados.html
```

O resumo consolidado dos resultados do pipeline está em:

```text
journal_execution_pipeline/RESULTS_SUMMARY.md
```
