from pathlib import Path
from PIL import Image
import pandas as pd

PROJECT_DIR = Path(".").resolve()
IMAGES_DIR = PROJECT_DIR / "data" / "raw" / "train_images"

image_info = []

for image_path in IMAGES_DIR.glob("*.png"):
    with Image.open(image_path) as img:
        width, height = img.size

    image_info.append({
        "arquivo": image_path.name,
        "largura": width,
        "altura": height,
        "resolucao": f"{width}x{height}"
    })

df_sizes = pd.DataFrame(image_info)

print("Total de imagens analisadas:", len(df_sizes))
print("\nResoluções mais frequentes:")
print(df_sizes["resolucao"].value_counts().head(20))

print("\nMenor largura:", df_sizes["largura"].min())
print("Maior largura:", df_sizes["largura"].max())
print("Menor altura:", df_sizes["altura"].min())
print("Maior altura:", df_sizes["altura"].max())

df_sizes.to_csv("results/metrics/image_original_sizes.csv", index=False)

summary = df_sizes[["largura", "altura"]].describe()
print(summary)