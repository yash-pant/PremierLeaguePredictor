from sklearn.metrics import accuracy_score
from data_generator import generate_synthetic_data
from feature_engineering import select_features
from model import load_model


def main():
    df = generate_synthetic_data()

    X = select_features(df)
    y = df["is_champion"]

    model = load_model()
    preds = model.predict(X)

    acc = accuracy_score(y, preds)
    print("Training Accuracy:", round(acc, 3))


if __name__ == "__main__":
    main()
