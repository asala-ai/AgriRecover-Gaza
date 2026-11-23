
import joblib
import tensorflow as tf


def load_model_and_scaler(model_path, scaler_path):
    """
    Load the trained ANN model and fitted StandardScaler.
    """

    model = tf.keras.models.load_model(
        model_path,
        compile=False
    )

    scaler = joblib.load(scaler_path)

    return model, scaler
