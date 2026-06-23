# journal_execution_pipeline

Pasta separada para executar novamente os prompts do artigo da revista com
modelos atuais ou com os modelos originais, sem misturar essa parte com os
scripts de analise do repositorio.

## O que esta pasta faz

- Le os `questions.json` ja existentes em `results/...`.
- Chama modelos via OpenAI, Gemini ou Ollama.
- Salva uma SQL por linha em um arquivo de saida.
- Registra metadados da execucao em JSON.
- Roda a avaliacao adaptada do Bruno para calcular scores de execucao.

## Estrutura

```text
journal_execution_pipeline/
  README.md
  requirements.txt
  configs/
    execution.example.json
  src/
    run_generation.py
    run_evaluation.py
    normalize_sql.py
    io_utils.py
    providers/
      __init__.py
      base.py
      openai_provider.py
      gemini_provider.py
      ollama_provider.py
  evaluation_tools/
    test-suite-sql-eval-en/
    test-suite-sql-eval-pt/
```

## Como usar

1. Copie o arquivo de configuracao exemplo.
2. Ajuste modelos, caminhos e chaves.
3. Rode o gerador como modulo Python.

Exemplo:

```bash
python -m journal_execution_pipeline.src.run_generation \
  --config journal_execution_pipeline/configs/execution.local.json
```

Para rodar so o Llama3 agora, use o config `execution.ollama.json`:

```bash
python -m journal_execution_pipeline.src.run_generation \
  --config journal_execution_pipeline/configs/execution.ollama.json
```

Para escolher apenas alguns modelos ou provedores dentro de um config maior:

```bash
python -m journal_execution_pipeline.src.run_generation \
  --config journal_execution_pipeline/configs/execution.example.json \
  --provider ollama
```

Voce tambem pode filtrar por `--run-name` ou `--model`. Esses filtros podem ser
repetidos.

## Como avaliar

Antes da avaliacao, instale as dependencias desta pasta no ambiente virtual:

```bash
pip install -r journal_execution_pipeline/requirements.txt
```

Para calcular Execution Accuracy (EX) das novas saidas do Llama3 em ingles:

```bash
python -m journal_execution_pipeline.src.run_evaluation \
  --language en \
  --predictions journal_execution_pipeline/outputs/ollama_en_0shot_llama3/RESULTS_MODEL-llama3.txt \
  --etype exec
```

Para portugues:

```bash
python -m journal_execution_pipeline.src.run_evaluation \
  --language pt \
  --predictions journal_execution_pipeline/outputs/ollama_pt_0shot_llama3/RESULTS_MODEL-llama3.txt \
  --etype exec
```

Para calcular Exact Match (EM), troque `--etype exec` por `--etype match`.

Os resultados sao salvos em `journal_execution_pipeline/evaluation_outputs/`.

## Variaveis de ambiente

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`

O Ollama roda localmente e nao precisa de chave, apenas do servidor ativo em
`http://localhost:11434`. Se o servidor nao estiver em execucao, suba com
`ollama serve` antes de rodar o pipeline.

## Observacao

O avaliador escreve `score.tsv` e, para `exec`, tambem `score_time.tsv`.
