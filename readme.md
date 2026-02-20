# Premier League Winner Predictor

A Python machine learning project that predicts the Premier League champion using squad-level features such as squad value, squad depth, and team strength indicators.

The model learns what a title-winning squad looks like and assigns a probability that each team wins the league.

This is a pipeline demonstration project, not a betting tool.

------------------------------------------------------------

FEATURES USED

- Squad market value
- Average age
- Wage index
- Squad depth
- Injury risk
- Manager stability
- Attack strength
- Defense strength

------------------------------------------------------------

SETUP

Clone the repository:

    git clone https://github.com/YOUR_USERNAME/premier-league-winner-model.git
    cd premier-league-winner-model

Create a virtual environment:

    python -m venv venv

Activate it:

Mac / Linux:
    source venv/bin/activate

Windows:
    venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

------------------------------------------------------------

TRAIN MODEL (synthetic seasons)

    python src/train.py

The trained model will be saved to:

    models/champion_model.joblib

------------------------------------------------------------

PREDICT WINNER (sample data)

    python src/predict.py

Input file:

    data/sample_season.json

------------------------------------------------------------

REAL DATA MODE (Transfermarkt via API provider)

This project does NOT directly scrape Transfermarkt pages.
It uses a structured API provider (Apify actor) that returns squad data.

Create environment file:

    cp .env.example .env

Edit .env and add your token:

    APIFY_TOKEN=your_token_here
    APIFY_ACTOR_ID=webdatalabs/transfermarkt-scraper

Run prediction:

    python src/predict.py --use_transfermarkt --season 2024-2025

------------------------------------------------------------

EVALUATE MODEL

    python src/evaluate.py

------------------------------------------------------------

PROJECT STRUCTURE

premier-league-winner-model/
    data/
    models/
    src/
        config.py
        data_generator.py
        feature_engineering.py
        model.py
        train.py
        predict.py
        evaluate.py
        tm_apify.py
        tm_normalize.py
    tests/

------------------------------------------------------------

NOTES

- Training uses generated historical seasons
- Real squad prediction uses API data
- This is a portfolio ML pipeline demo

------------------------------------------------------------
