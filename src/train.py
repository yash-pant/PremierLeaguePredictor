from data_generator import generate_synthetic_data
from feature_engineering import select_features
from model import build_model, save_model


def main():
    df = generate_synthetic_data()

    X = select_features(df)
    y = df["is_champion"]

    model = build_model()
    model.fit(X, y)

    save_model(model)
    print("Model trained and saved successfully.")


if __name__ == "__main__":
    main()
