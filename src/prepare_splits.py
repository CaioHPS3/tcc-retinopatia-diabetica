import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

PROJECT_DIR = Path(__file__).resolve().parents[1]

TRAIN_CSV = PROJECT_DIR / "data" / "raw" / "train.csv"
TRAIN_IMAGES_DIR = PROJECT_DIR / "data" / "raw" / "train_images"

SPLITS_DIR = PROJECT_DIR / "data" / "splits"
SPLITS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42


def main():
    df = pd.read_csv(TRAIN_CSV)

    df["image_path"] = df["id_code"].apply(
        lambda image_id: str(TRAIN_IMAGES_DIR / f"{image_id}.png")
    )

    df["image_exists"] = df["image_path"].apply(lambda path: Path(path).exists())
    missing_images = df[df["image_exists"] == False]

    if not missing_images.empty:
        print("Algumas imagens do train.csv não foram encontradas:")
        print(missing_images[["id_code", "image_path"]])
        raise FileNotFoundError(
            "Existem imagens ausentes. Verifique a base antes de continuar."
        )

    df = df.drop(columns=["image_exists"])

    # Primeira divisão: 60% treino e 40% temporário.
    train_df, temp_df = train_test_split(
        df,
        test_size=0.40,
        stratify=df["diagnosis"],
        random_state=SEED
    )

    # Segunda divisão: divide os 40% temporários em 20% validação e 20% teste.
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        stratify=temp_df["diagnosis"],
        random_state=SEED
    )

    train_df.to_csv(SPLITS_DIR / "train_split.csv", index=False)
    val_df.to_csv(SPLITS_DIR / "val_split.csv", index=False)
    test_df.to_csv(SPLITS_DIR / "test_split.csv", index=False)

    print("Divisão estratificada concluída com sucesso.")
    print(f"Total da base: {len(df)} imagens")
    print(f"Treino: {len(train_df)} imagens")
    print(f"Validação: {len(val_df)} imagens")
    print(f"Teste: {len(test_df)} imagens")

    print("\nDistribuição por classe - Base original:")
    print(df["diagnosis"].value_counts().sort_index())

    print("\nDistribuição por classe - Treino:")
    print(train_df["diagnosis"].value_counts().sort_index())

    print("\nDistribuição por classe - Validação:")
    print(val_df["diagnosis"].value_counts().sort_index())

    print("\nDistribuição por classe - Teste:")
    print(test_df["diagnosis"].value_counts().sort_index())

    print("\nPercentual por classe - Treino:")
    print((train_df["diagnosis"].value_counts(normalize=True).sort_index() * 100).round(2))

    print("\nPercentual por classe - Validação:")
    print((val_df["diagnosis"].value_counts(normalize=True).sort_index() * 100).round(2))

    print("\nPercentual por classe - Teste:")
    print((test_df["diagnosis"].value_counts(normalize=True).sort_index() * 100).round(2))


if __name__ == "__main__":
    main()
