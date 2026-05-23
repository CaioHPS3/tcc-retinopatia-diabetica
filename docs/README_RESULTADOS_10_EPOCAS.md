# Comparação inicial dos modelos — 10 épocas

Configuração utilizada:

- Divisão: 60% treino / 20% validação / 20% teste
- Épocas: 10
- Batch size: 16
- Tamanho das imagens: 224 x 224
- GPU utilizada: não

Resumo dos resultados:

| modelo         |   test_loss |   test_accuracy |   test_accuracy_percent |   macro_precision |   macro_recall |   macro_f1 |   weighted_precision |   weighted_recall |   weighted_f1 |   epochs_completed |   batch_size | image_size   | split_strategy                         | gpu_available   |
|:---------------|------------:|----------------:|------------------------:|------------------:|---------------:|-----------:|---------------------:|------------------:|--------------:|-------------------:|-------------:|:-------------|:---------------------------------------|:----------------|
| ResNet50       |    0.823445 |        0.680764 |                   68.08 |            0.5241 |         0.5892 |     0.522  |               0.7277 |            0.6808 |        0.6757 |                 10 |           16 | 224x224      | 60% treino / 20% validação / 20% teste | False           |
| EfficientNetB0 |    0.940062 |        0.630034 |                   63    |            0.4749 |         0.5004 |     0.4577 |               0.6617 |            0.6412 |        0.6183 |                 10 |           16 | 224x224      |                                        |                 |
| DenseNet121    |    1.04162  |        0.593452 |                   59.35 |            0.4905 |         0.523  |     0.429  |               0.7296 |            0.5935 |        0.5875 |                 10 |           16 | 224x224      | 60% treino / 20% validação / 20% teste | False           |

Interpretação inicial:

- A ResNet50 apresentou a maior acurácia de teste entre os três modelos.
- A EfficientNetB0 ficou em segundo lugar na acurácia geral.
- A DenseNet121 teve menor acurácia geral, embora tenha apresentado recall macro ligeiramente superior ao da EfficientNetB0.
- A acurácia isolada não deve ser a única métrica analisada, pois a base possui desbalanceamento entre classes.
