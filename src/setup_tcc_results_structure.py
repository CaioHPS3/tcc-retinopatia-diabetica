#!/usr/bin/env python3
"""
Cria a nova estrutura de organização dos experimentos do TCC.

Execute a partir da raiz do projeto:

    python setup_tcc_results_structure.py

Estrutura criada:

results/
  metrics/<tecnica>/<modelo>/
  figures/<tecnica>/<modelo>/
models/<tecnica>/<modelo>/
notebooks/<modelo>/

O script não apaga e não move arquivos antigos automaticamente.
"""

from pathlib import Path

TECHNIQUES = {
    "t1_blocos_finais": "Fine-tuning dos blocos finais",
    "t2_blocos_intermediarios_finais": "Fine-tuning dos blocos intermediários e finais",
    "t3_blocos_amplos_profundos": "Fine-tuning amplo/profundo",
}

MODELS = [
    "efficientnetb0",
    "resnet50",
    "densenet121",
]


def find_project_dir() -> Path:
    cwd = Path.cwd().resolve()
    if cwd.name == "notebooks":
        return cwd.parent
    return cwd


def main() -> None:
    project_dir = find_project_dir()

    results_dir = project_dir / "results"
    metrics_dir = results_dir / "metrics"
    figures_dir = results_dir / "figures"
    models_dir = project_dir / "models"
    notebooks_dir = project_dir / "notebooks"

    created_dirs = []

    for technique in TECHNIQUES:
        for model in MODELS:
            paths = [
                metrics_dir / technique / model,
                figures_dir / technique / model,
                models_dir / technique / model,
            ]
            for path in paths:
                path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(path)

    for model in MODELS:
        path = notebooks_dir / model
        path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(path)

    readme_path = results_dir / "README_ESTRUTURA_EXPERIMENTOS.md"
    readme_text = "# Estrutura dos experimentos\n\n"
    readme_text += "Esta pasta organiza os resultados por técnica de fine-tuning e arquitetura.\n\n"
    readme_text += "## Técnicas\n\n"
    for technique, description in TECHNIQUES.items():
        readme_text += f"- `{technique}`: {description}.\n"
    readme_text += "\n## Modelos\n\n"
    for model in MODELS:
        readme_text += f"- `{model}`\n"
    readme_text += "\n## Estrutura\n\n"
    readme_text += "```text\n"
    readme_text += "results/metrics/<tecnica>/<modelo>/\n"
    readme_text += "results/figures/<tecnica>/<modelo>/\n"
    readme_text += "models/<tecnica>/<modelo>/\n"
    readme_text += "notebooks/<modelo>/\n"
    readme_text += "```\n\n"
    readme_text += "Arquivos antigos na raiz de `results/metrics` não são movidos automaticamente por segurança.\n"

    results_dir.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(readme_text, encoding="utf-8")

    print("Estrutura criada/verificada em:", project_dir)
    print("\nPastas principais:")
    print("-", metrics_dir)
    print("-", figures_dir)
    print("-", models_dir)
    print("-", notebooks_dir)
    print("\nREADME criado em:", readme_path)
    print("\nTotal de diretórios verificados/criados:", len(created_dirs))


if __name__ == "__main__":
    main()
