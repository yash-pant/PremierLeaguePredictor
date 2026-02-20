from sklearn.ensemble import RandomForestClassifier
import joblib
from config import MODEL_PATH


def build_model():
    return RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )


def save_model(model):
    joblib.dump(model, MODEL_PATH)


def load_model():
    return joblib.load(MODEL_PATH)
