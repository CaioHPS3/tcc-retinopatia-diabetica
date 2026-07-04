from pathlib import Path
from PIL import Image
import pandas as pd

# ============================================================
# Caminhos
# ============================================================

PROJECT_DIR = Path(".").resolve()

TRAIN_CSV_PATH = PROJECT_DIR / "data" / "raw" / "train.csv"
IMAGES_DIR = PROJECT_DIR / "data" / "raw" / "train_images"

OUTPUT_DIR = PROJECT_DIR / "results" / "metrics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Nomes das classes
# ============================================================

CLASS_NAMES = {
    0: "Sem retinopatia",
    1: "Retinopatia leve",
    2: "Retinopatia moderada",
    3: "Retinopatia severa",
    4: "Retinopatia proliferativa",
}

# ============================================================
# Leitura do train.csv
# ============================================================

train_df = pd.read_csv(TRAIN_CSV_PATH)

# Garante que o nome da imagem tenha extensão .png
train_df["arquivo"] = train_df["id_code"].astype(str) + ".png"
train_df["image_path"] = train_df["arquivo"].apply(lambda x: IMAGES_DIR / x)

# ============================================================
# Coleta das dimensões das imagens
# ============================================================

image_info = []

for _, row in train_df.iterrows():
    image_path = row["image_path"]

    if not image_path.exists():
        print(f"Imagem não encontrada: {image_path}")
        continue

    with Image.open(image_path) as img:
        width, height = img.size

    diagnosis = int(row["diagnosis"])

    image_info.append({
        "id_code": row["id_code"],
        "arquivo": image_path.name,
        "diagnosis": diagnosis,
        "classe": CLASS_NAMES.get(diagnosis, "Classe desconhecida"),
        "largura": width,
        "altura": height,
        "resolucao": f"{width}x{height}"
    })

df_sizes = pd.DataFrame(image_info)

# ============================================================
# Resumo geral
# ============================================================

print("=" * 80)
print("RESUMO GERAL DAS IMAGENS")
print("=" * 80)

print("Total de imagens analisadas:", len(df_sizes))

print("\nResoluções mais frequentes na base completa:")
print(df_sizes["resolucao"].value_counts().head(20))

print("\nMenor largura:", df_sizes["largura"].min())
print("Maior largura:", df_sizes["largura"].max())
print("Menor altura:", df_sizes["altura"].min())
print("Maior altura:", df_sizes["altura"].max())

print("\nEstatísticas gerais de largura e altura:")
print(df_sizes[["largura", "altura"]].describe())

# ============================================================
# Resumo por classe
# ============================================================

print("\n" + "=" * 80)
print("RESUMO POR CLASSE")
print("=" * 80)

class_summary = (
    df_sizes
    .groupby(["diagnosis", "classe"])
    .agg(
        quantidade=("arquivo", "count"),
        largura_min=("largura", "min"),
        largura_media=("largura", "mean"),
        largura_mediana=("largura", "median"),
        largura_max=("largura", "max"),
        altura_min=("altura", "min"),
        altura_media=("altura", "mean"),
        altura_mediana=("altura", "median"),
        altura_max=("altura", "max"),
    )
    .reset_index()
)

# Arredonda médias para facilitar leitura
class_summary["largura_media"] = class_summary["largura_media"].round(2)
class_summary["altura_media"] = class_summary["altura_media"].round(2)

print(class_summary)

# ============================================================
# Resoluções predominantes por classe
# ============================================================

print("\n" + "=" * 80)
print("RESOLUÇÕES MAIS FREQUENTES POR CLASSE")
print("=" * 80)

top_resolutions_by_class = []

for diagnosis, class_name in CLASS_NAMES.items():
    df_class = df_sizes[df_sizes["diagnosis"] == diagnosis]

    print(f"\nClasse {diagnosis} - {class_name}")
    print("-" * 80)

    resolution_counts = (
        df_class["resolucao"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    resolution_counts.columns = ["resolucao", "quantidade"]
    resolution_counts["diagnosis"] = diagnosis
    resolution_counts["classe"] = class_name
    resolution_counts["percentual_na_classe"] = (
        resolution_counts["quantidade"] / len(df_class) * 100
    ).round(2)

    print(resolution_counts[["resolucao", "quantidade", "percentual_na_classe"]])

    top_resolutions_by_class.append(resolution_counts)

top_resolutions_by_class_df = pd.concat(top_resolutions_by_class, ignore_index=True)

# ============================================================
# Resolução predominante principal de cada classe
# ============================================================

main_resolution_by_class = (
    top_resolutions_by_class_df
    .sort_values(["diagnosis", "quantidade"], ascending=[True, False])
    .groupby(["diagnosis", "classe"])
    .head(1)
    .reset_index(drop=True)
)

print("\n" + "=" * 80)
print("RESOLUÇÃO PREDOMINANTE DE CADA CLASSE")
print("=" * 80)

print(main_resolution_by_class[
    ["diagnosis", "classe", "resolucao", "quantidade", "percentual_na_classe"]
])

# ============================================================
# Salvamento dos arquivos
# ============================================================

df_sizes.to_csv(
    OUTPUT_DIR / "image_original_sizes_by_image.csv",
    index=False
)

class_summary.to_csv(
    OUTPUT_DIR / "image_original_sizes_summary_by_class.csv",
    index=False
)

top_resolutions_by_class_df.to_csv(
    OUTPUT_DIR / "image_original_top_resolutions_by_class.csv",
    index=False
)

main_resolution_by_class.to_csv(
    OUTPUT_DIR / "image_original_main_resolution_by_class.csv",
    index=False
)

print("\n" + "=" * 80)
print("ARQUIVOS SALVOS")
print("=" * 80)

print(OUTPUT_DIR / "image_original_sizes_by_image.csv")
print(OUTPUT_DIR / "image_original_sizes_summary_by_class.csv")
print(OUTPUT_DIR / "image_original_top_resolutions_by_class.csv")
print(OUTPUT_DIR / "image_original_main_resolution_by_class.csv")