## Transfermarkt (real data)

Direct scraping of Transfermarkt HTML is prohibited by their Terms, so this project uses an API-style extractor via Apify instead.

### Steps
1. Create an Apify account
2. Get your API token
3. Copy `.env.example` to `.env` and set:
   - APIFY_TOKEN=...
   - APIFY_ACTOR_ID=webdatalabs/transfermarkt-scraper (or another Transfermarkt actor you use)

### Run prediction using Transfermarkt squads
```bash
python src/predict.py --use_transfermarkt --season 2024-2025
(Hosted Transfermarkt scraping services exist on Apify.)  [oai_citation:1‡Apify](https://apify.com/webdatalabs/transfermarkt-scraper/api/python?utm_source=chatgpt.com)

---

## How you run it (no IDE needed)

1. Add the files above directly in GitHub (same folders).
2. Locally (or Codespaces), run:

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env with your APIFY_TOKEN
python src/train.py
python src/predict.py --use_transfermarkt --season 2024-2025
