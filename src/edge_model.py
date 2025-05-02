"""
edge_model.py
Lightweight edge‑inference helper: uses either a simple threshold
or a scikit‑learn model for overheating detection.
"""

from __future__ import annotations

import logging
import pathlib
from typing import Iterable, List

import joblib
import numpy as np
from sklearn.base import BaseEstimator

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class EdgeModel:
    """
    Parameters
    ----------
    model_path : str | pathlib.Path | None
        Path to a serialized scikit‑learn model (joblib format).
        If None, the class falls back to threshold mode.
    threshold : float, default 75.0
        Temperature threshold (°C) for simple rule‑based detection.

    Notes
    -----
    - Expects the model to accept a 2‑D array of shape (n_samples, 1).
    - If the model requires scaling, embed the scaler in a Pipeline
      when you joblib‑dump it (recommended).
    """

    def __init__(
        self,
        model_path: str | pathlib.Path | None = None,
        threshold: float = 75.0,
    ) -> None:
        self._model: BaseEstimator | None = None
        self._use_threshold = model_path is None
        self._threshold = threshold

        if model_path:
            try:
                self._model = joblib.load(model_path)
                logging.info("Loaded edge model from %s", model_path)
            except Exception as exc:  # broad catch OK for edge robustness
                logging.error("Model load failed (%s); reverting to threshold mode.", exc)
                self._use_threshold = True

    # ------------------------------------------------------------------
    def _predict_single(self, temp_c: float) -> bool:
        if self._use_threshold:
            return temp_c >= self._threshold
        assert self._model is not None  # mypy/static‑type safety
        return bool(self._model.predict(np.array([[temp_c]]))[0])

    # ------------------------------------------------------------------
    def predict_overheat(self, temp_c: float | Iterable[float]) -> List[bool]:
        """
        Predict overheating for a single reading or an iterable of readings.

        Returns
        -------
        List[bool]
            True for overheat, False otherwise, preserving input order.
        """
        if isinstance(temp_c, Iterable):
            return [self._predict_single(t) for t in temp_c]  # type: ignore[arg‑type]
        return [self._predict_single(temp_c)]


# ------------------------- CLI demo -------------------------
if __name__ == "__main__":
    temps = [72.3, 75.9, 78.0]  # °C
    model = EdgeModel(threshold=75.0)  # or EdgeModel("model.joblib")
    print(model.predict_overheat(temps))
