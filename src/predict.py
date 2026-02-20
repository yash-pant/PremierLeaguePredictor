import argparse
import pandas as pd

from model import load_model
from feature_engineering import select_features

from tm_apify import get_premier_league_squads_from_transfermarkt
from tm_normalize import normalize_apify_items_to_team_rows


def predict_winner(df: pd.DataFrame) -> pd.DataFrame:
    model = load_model()

    X = select_features(df)
    probs = model.predict_proba(X)[:, 1]

    out = df.copy()
    out["champion_probability"] = probs
    return out.sort_values("champion_probability", ascending=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--season_json", default="data/sample_season.json", help="Local season JSON (team rows)")
    parser.add_argument("--use_transfermarkt", action="store_true", help="Fetch squads via Apify/Transfermarkt")
    parser.add_argument("--season", default=None, help="Season like '2024-2025' (used with --use_transfermarkt)")
    args = parser.parse_args()

    if args.use_transfermarkt:
        season = args.season or "2024-2025"
        items = get_premier_league_squads_from_transfermarkt(season=season)
        rows = normalize_apify_items_to_team_rows(items)
        season_data = pd.DataFrame(rows)

        # Fill the rest of required features with placeholders
        # (You can enrich later with more real signals.)
        for col, default in [
            ("wage_index", 70.0),
            ("injury_risk", 20.0),
            ("manager_stability", 75.0),
            ("attack_index", 75.0),
            ("defense_index", 75.0),
        ]:
            if col not in season_data.columns:
                season_data[col] = default
    else:
        season_data = pd.read_json(args.season_json)

    ranked = predict_winner(season_data)
    winner = ranked.iloc[0]

    print("Predicted Champion:", winner["team"])
    print("Probability:", round(float(winner["champion_probability"]), 3))
    print("\nTop 5:")
    print(ranked[["team", "champion_probability"]].head(5).to_string(index=False))


if __name__ == "__main__":
    main()
