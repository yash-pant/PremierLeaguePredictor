import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_API_BASE = "https://api.apify.com/v2"


class TransfermarktProviderError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    val = os.getenv(name, "").strip()
    if not val:
        raise TransfermarktProviderError(
            f"Missing env var {name}. Create a .env file (see .env.example)."
        )
    return val


def run_actor_and_get_dataset_id(actor_id: str, token: str, actor_input: dict) -> str:
    """
    Runs an Apify actor and returns the output dataset ID.
    """
    url = f"{APIFY_API_BASE}/acts/{actor_id}/runs?token={token}"
    resp = requests.post(url, json=actor_input, timeout=120)
    if resp.status_code >= 300:
        raise TransfermarktProviderError(
            f"Apify run failed ({resp.status_code}): {resp.text[:300]}"
        )

    run = resp.json().get("data", {})
    run_id = run.get("id")
    if not run_id:
        raise TransfermarktProviderError("Apify response missing run id.")

    # Wait for run to finish
    status_url = f"{APIFY_API_BASE}/actor-runs/{run_id}?token={token}"
    while True:
        s = requests.get(status_url, timeout=60).json().get("data", {})
        status = s.get("status")
        if status in ("SUCCEEDED", "FAILED", "TIMED-OUT", "ABORTED"):
            if status != "SUCCEEDED":
                raise TransfermarktProviderError(f"Apify run ended with status={status}")
            dataset_id = s.get("defaultDatasetId")
            if not dataset_id:
                raise TransfermarktProviderError("Apify run missing defaultDatasetId.")
            return dataset_id
        time.sleep(2)


def fetch_dataset_items(dataset_id: str, token: str, limit: int = 1000) -> list[dict]:
    """
    Fetches items from an Apify dataset.
    """
    url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items?token={token}&clean=true&limit={limit}"
    resp = requests.get(url, timeout=120)
    if resp.status_code >= 300:
        raise TransfermarktProviderError(
            f"Dataset fetch failed ({resp.status_code}): {resp.text[:300]}"
        )
    return resp.json()


def get_premier_league_squads_from_transfermarkt(season: str) -> list[dict]:
    """
    Uses an Apify Transfermarkt actor to fetch squads for PL season.

    Output: list of clubs, each with players and squad totals (depending on actor).
    NOTE: Exact fields vary by actor. We normalize later in tm_normalize.py.
    """
    token = _require_env("APIFY_TOKEN")
    actor_id = os.getenv("APIFY_ACTOR_ID", "webdatalabs/transfermarkt-scraper").strip()

    # Actor inputs vary between actors; this is a common pattern.
    # If your chosen actor expects different keys, tweak here.
    actor_input = {
        "mode": "competitionSquads",
        "competition": "premier-league",
        "season": season,
        "includePlayers": True,
        "includeMarketValues": True,
    }

    dataset_id = run_actor_and_get_dataset_id(actor_id=actor_id, token=token, actor_input=actor_input)
    items = fetch_dataset_items(dataset_id=dataset_id, token=token)
    if not isinstance(items, list) or len(items) == 0:
        raise TransfermarktProviderError("No items returned from dataset.")
    return items
