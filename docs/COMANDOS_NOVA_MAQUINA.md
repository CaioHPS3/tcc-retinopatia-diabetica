# Comandos para preparar uma nova máquina

Este arquivo registra os comandos necessários para configurar o projeto em uma nova máquina.

## 1. Instalar dependências do sistema no Ubuntu

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

## 2. Clonar o projeto

Substitua a URL se o repositório for diferente.

```bash
git clone https://github.com/CaioHPS3/tcc-retinopatia-diabetica.git
cd tcc-retinopatia-diabetica
```

## 3. Criar e ativar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 4. Instalar bibliotecas Python

Opção usando `requirements.txt`, se ele existir:

```bash
pip install -r requirements.txt
```

Opção manual:

```bash
pip install pandas numpy matplotlib pillow scikit-learn ipykernel tensorflow
```

Em máquina Linux com GPU NVIDIA e ambiente compatível com CUDA, testar:

```bash
pip install "tensorflow[and-cuda]"
```

## 5. Registrar kernel para o VS Code/Jupyter

```bash
python -m ipykernel install --user --name tcc-retinopatia --display-name "Python (TCC Retinopatia)"
```

No VS Code, selecione o kernel:

```text
Python (TCC Retinopatia)
```

## 6. Baixar e posicionar a base APTOS

A base não deve ficar no GitHub. Coloque os arquivos nesta estrutura:

```text
data/
└── raw/
    ├── train.csv
    ├── test.csv
    ├── sample_submission.csv
    ├── train_images/
    └── test_images/
```

Conferir quantidade de imagens de treino:

```bash
find data/raw/train_images -maxdepth 1 -name "*.png" | wc -l
```

O esperado para a APTOS 2019 é:

```text
3662
```

## 7. Gerar splits 60/20/20

```bash
python src/prepare_splits.py
```

Arquivos esperados:

```text
data/splits/train_split.csv
data/splits/val_split.csv
data/splits/test_split.csv
```

## 8. Ordem recomendada dos notebooks

```text
01_exploracao_base.ipynb
02_carregamento_imagens.ipynb
03_pipeline_tensorflow.ipynb
04_treino_efficientnetb0.ipynb
05_treino_resnet50.ipynb
06_treino_densenet121.ipynb
```

## 9. Organizar resultados depois dos treinos

Depois de rodar os três modelos, execute:

```bash
python src/organize_results.py --experiment baseline_10ep_cpu_60_20_20
```

A estrutura será criada em:

```text
results/experiments/baseline_10ep_cpu_60_20_20/
```

## 10. Enviar alterações para o GitHub

```bash
git status
git add .
git commit -m "Atualiza notebooks e scripts do projeto"
git push
```

Antes do `git add .`, confira se a base de imagens, ambiente virtual e modelos treinados estão no `.gitignore`.
