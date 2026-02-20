from src.data_generator import generate_synthetic_data
from src.feature_engineering import select_features


def test_feature_shape():
    df = generate_synthetic_data(n_seasons=1)
    X = select_features(df)
    assert X.shape[1] == 8
