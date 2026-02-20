import numpy as np
import pandas as pd
from config import RANDOM_SEED

np.random.seed(RANDOM_SEED)


def generate_synthetic_data(n_seasons=15, teams_per_season=20):
    rows = []

    for season in range(2008, 2008 + n_seasons):
        for team_id in range(teams_per_season):
            squad_value = np.random.normal(600, 200)
            attack = np.random.normal(75, 10)
            defense = np.random.normal(75, 10)

            strength_score = (
                squad_value * 0.4
                + attack * 50
                + defense * 40
                - np.random.normal(0, 100)
            )

            rows.append({
                "season": season,
                "team": f"Team_{team_id}",
                "squad_value_m": squad_value,
                "avg_age": np.random.normal(26, 2),
                "wage_index": np.random.normal(70, 15),
                "squad_depth": np.random.normal(75, 10),
                "injury_risk": np.random.normal(20, 5),
                "manager_stability": np.random.normal(80, 10),
                "attack_index": attack,
                "defense_index": defense,
                "strength_score": strength_score
            })

    df = pd.DataFrame(rows)

    # Label champion per season
    df["is_champion"] = df.groupby("season")["strength_score"] \
        .transform(lambda x: x == x.max()).astype(int)

    return df
