from __future__ import annotations

import re


def _parse_money_to_millions(value) -> float | None:
    """
    Converts Transfermarkt-style money strings to millions (e.g., '€1.2bn', '€450m', '€900k').
    Returns None if unknown.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        # assume already in millions if it's a big number; otherwise treat as-is
        return float(value)

    s = str(value).strip().lower()
    if not s or s in {"-", "n/a", "na", "unknown"}:
        return None

    # remove currency symbols and spaces
    s = s.replace("€", "").replace("$", "").replace("£", "").replace(",", "").strip()

    m = re.match(r"^([0-9]*\.?[0-9]+)\s*(bn|b|m|k)?$", s)
    if not m:
        return None

    num = float(m.group(1))
    unit = m.group(2)

    if unit in ("bn", "b"):
        return num * 1000.0
    if unit == "m" or unit is None:
        return num
    if unit == "k":
        return num / 1000.0
    return None


def normalize_apify_items_to_team_rows(apify_items: list[dict]) -> list[dict]:
    """
    Tries to normalize different Transfermarkt Apify actor outputs into simple team rows:
      {team, squad_value_m, avg_age, squad_depth, ...}

    Many actors will return:
      - clubName / club
      - players: list with age, marketValue, ...
      - squadMarketValue / totalMarketValue, etc.

    We compute:
      - squad_value_m from total if available else sum of player values
      - avg_age from player ages if available
      - squad_depth from number of players
    """
    team_rows: list[dict] = []

    for item in apify_items:
        team = (
            item.get("clubName")
            or item.get("club")
            or item.get("team")
            or item.get("name")
            or "Unknown Club"
        )

        players = item.get("players") or item.get("squad") or []
        if not isinstance(players, list):
            players = []

        # total market value fields (vary by actor)
        total_mv_raw = (
            item.get("squadMarketValue")
            or item.get("totalMarketValue")
            or item.get("marketValue")
            or item.get("squad_value")
        )
        total_mv_m = _parse_money_to_millions(total_mv_raw)

        # fallback: sum player market values
        if total_mv_m is None and players:
            s = 0.0
            count = 0
            for p in players:
                mv = _parse_money_to_millions(p.get("marketValue") or p.get("market_value"))
                if mv is not None:
                    s += mv
                    count += 1
            if count > 0:
                total_mv_m = s

        # avg age
        ages = []
        for p in players:
            age = p.get("age")
            try:
                if age is not None:
                    ages.append(float(age))
            except Exception:
                pass
        avg_age = sum(ages) / len(ages) if ages else None

        squad_depth = len(players) if players else None

        team_rows.append(
            {
                "team": team,
                "squad_value_m": float(total_mv_m) if total_mv_m is not None else 0.0,
                "avg_age": float(avg_age) if avg_age is not None else 26.0,
                "squad_depth": float(squad_depth) if squad_depth is not None else 22.0,
            }
        )

    return team_rows
