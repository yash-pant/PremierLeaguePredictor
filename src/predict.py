import pandas as pd
from model import load_model
from feature_engineering import select_features


def main():
    model = load_model()
    season_data = pd.read_json("data/sample_season.json")

    X = select_features(season_data)
    probs = model.predict_proba(X)[:, 1]

    season_data["champion_probability"] = probs

    winner = season_data.sort_values(
        "champion_probability",
        ascending=False
    ).iloc[0]

    print("Predicted Champion:", winner["team"])
    print("Probability:", round(winner["champion_probability"], 3))


if __name__ == "__main__":
    main()
