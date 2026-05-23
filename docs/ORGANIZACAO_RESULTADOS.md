# Organização recomendada dos resultados

## Estrutura sugerida

```text
results/
├── comparison/
│   └── comparacao_modelos_10_epocas_60_20_20_cpu.csv
└── experiments/
    └── baseline_10ep_cpu_60_20_20/
        ├── efficientnetb0/
        │   ├── metrics/
        │   │   ├── efficientnetb0_classification_report.txt
        │   │   ├── efficientnetb0_confusion_matrix.csv
        │   │   ├── efficientnetb0_history.csv
        │   │   └── efficientnetb0_summary_metrics.json
        │   ├── figures/
        │   └── model/
        ├── resnet50/
        │   ├── metrics/
        │   ├── figures/
        │   └── model/
        └── densenet121/
            ├── metrics/
            ├── figures/
            └── model/
```

## Por que organizar assim?

Cada experimento fica isolado pelo nome da configuração usada. Por exemplo:

```text
baseline_10ep_cpu_60_20_20
```

Esse nome registra que o experimento foi feito como linha de base, com 10 épocas, em CPU, usando divisão 60/20/20.

Se depois você testar GPU, fine-tuning ou filtro gaussiano, crie outras pastas:

```text
baseline_30ep_gpu_60_20_20
finetuning_10ep_gpu_60_20_20
gaussian_preprocess_10ep_gpu_60_20_20
```

Isso evita misturar resultados de configurações diferentes.
