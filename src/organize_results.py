"""
Organiza resultados de experimentos do TCC.

Uso recomendado, na raiz do projeto:
    python src/organize_results.py --experiment baseline_10ep_cpu_60_20_20

O script copia arquivos de:
    results/metrics/
    results/figures/
    models/

Para:
    results/experiments/<experiment>/<modelo>/

Ele não apaga os arquivos originais.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Iterable

MODEL_KEYS = ["efficientnetb0", "resnet50", "densenet121"]


def copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)

    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

    return True


def collect_metrics_row(summary_path: Path, report_path: Path) -> dict:
    row = {}

    if summary_path.exists():
        with summary_path.open("r", encoding="utf-8") as f:
            summary = json.load(f)

        row.update({
            "modelo": summary.get("model"),
            "test_loss": summary.get("test_loss"),
            "test_accuracy": summary.get("test_accuracy"),
            "epochs_completed": summary.get("epochs_completed", summary.get("epochs_configured")),
            "batch_size": summary.get("batch_size"),
            "image_size": "x".join(map(str, summary.get("image_size", []))),
            "split_strategy": summary.get("split_strategy"),
            "gpu_available": summary.get("gpu_available"),
        })

    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--experiment",
        default="baseline_10ep_cpu_60_20_20",
        help="Nome da pasta do experimento dentro de results/experiments/"
    )
    args = parser.parse_args()

    project_dir = Path.cwd()
    results_dir = project_dir / "results"
    metrics_dir = results_dir / "metrics"
    figures_dir = results_dir / "figures"
    models_dir = project_dir / "models"

    experiment_dir = results_dir / "experiments" / args.experiment
    comparison_dir = results_dir / "comparison"
    comparison_dir.mkdir(parents=True, exist_ok=True)

    copied_any = False
    summary_rows = []

    for model_key in MODEL_KEYS:
        model_dir = experiment_dir / model_key

        metric_files = [
            f"{model_key}_classification_report.txt",
            f"{model_key}_confusion_matrix.csv",
            f"{model_key}_history.csv",
            f"{model_key}_summary_metrics.json",
        ]

        figure_patterns = [
            f"{model_key}_confusion_matrix.png",
            f"{model_key}_loss.png",
            f"{model_key}_accuracy.png",
            f"{model_key}_*.png",
        ]

        for filename in metric_files:
            copied_any |= copy_if_exists(
                metrics_dir / filename,
                model_dir / "metrics" / filename
            )

        seen_figures = set()
        for pattern in figure_patterns:
            for fig_path in figures_dir.glob(pattern):
                if fig_path.name in seen_figures:
                    continue
                seen_figures.add(fig_path.name)
                copied_any |= copy_if_exists(
                    fig_path,
                    model_dir / "figures" / fig_path.name
                )

        copied_any |= copy_if_exists(
            models_dir / model_key,
            model_dir / "model"
        )

        row = collect_metrics_row(
            metrics_dir / f"{model_key}_summary_metrics.json",
            metrics_dir / f"{model_key}_classification_report.txt"
        )
        if row:
            summary_rows.append(row)

    if summary_rows:
        import csv

        output_csv = comparison_dir / f"{args.experiment}_summary.csv"
        fieldnames = [
            "modelo",
            "test_loss",
            "test_accuracy",
            "epochs_completed",
            "batch_size",
            "image_size",
            "split_strategy",
            "gpu_available",
        ]

        with output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary_rows:
                writer.writerow({key: row.get(key) for key in fieldnames})

        print(f"Resumo salvo em: {output_csv}")

    if copied_any:
        print(f"Resultados organizados em: {experiment_dir}")
    else:
        print("Nenhum arquivo foi copiado. Verifique se os resultados estão em results/metrics e results/figures.")


if __name__ == "__main__":
    main()
