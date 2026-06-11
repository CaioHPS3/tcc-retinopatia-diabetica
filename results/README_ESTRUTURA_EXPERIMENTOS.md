# Estrutura dos experimentos

Esta pasta organiza os resultados por técnica de fine-tuning e arquitetura.

## Técnicas

- `t1_blocos_finais`: Fine-tuning dos blocos finais.
- `t2_blocos_intermediarios_finais`: Fine-tuning dos blocos intermediários e finais.
- `t3_blocos_amplos_profundos`: Fine-tuning amplo/profundo.

## Modelos

- `efficientnetb0`
- `resnet50`
- `densenet121`

## Estrutura

```text
results/metrics/<tecnica>/<modelo>/
results/figures/<tecnica>/<modelo>/
models/<tecnica>/<modelo>/
notebooks/<modelo>/
```

Arquivos antigos na raiz de `results/metrics` não são movidos automaticamente por segurança.
