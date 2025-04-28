"""
Edge inference: simple threshold or ML model.
"""
import pickle

class EdgeModel:
    def __init__(self, model_path=None, threshold=75.0):
        if model_path:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.use_threshold = False
        else:
            self.threshold = threshold
            self.use_threshold = True

    def predict_overheat(self, temp_c: float) -> bool:
        if self.use_threshold:
            return temp_c >= self.threshold
        return bool(self.model.predict([[temp_c]])[0])