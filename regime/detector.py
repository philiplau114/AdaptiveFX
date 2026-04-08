"""
HMM + SVM regime detection module for AdaptiveFX.

Uses a Hidden Markov Model to identify latent market states and a Support
Vector Machine to classify those states into the three canonical regimes
used by the strategy mapping layer.
"""

from __future__ import annotations

from collections import deque

import pandas as pd
from loguru import logger

# Regime label constants (mirrors config/pairs.py for convenience)
TRENDING: str = "TRENDING"
MEAN_REVERTING: str = "MEAN_REVERTING"
BREAKOUT: str = "BREAKOUT"


class RegimeDetector:
    """Combines HMM hidden-state discovery with SVM regime classification.

    Attributes:
        hmm_model: Trained GaussianHMM instance (set after ``train()``).
        svm_model: Trained SVC instance (set after ``train()``).
    """

    def __init__(self) -> None:
        self.hmm_model = None
        self.svm_model = None

    # ------------------------------------------------------------------
    def train(self, df: pd.DataFrame) -> None:
        """Train the HMM and SVM on historical OHLCV data.

        Feature extraction, HMM fitting, and SVM training are delegated to
        :class:`regime.trainer.RegimeTrainer`.  This method serves as a
        convenience wrapper for the detector.

        Args:
            df: Historical OHLCV DataFrame with a DatetimeIndex.
        """
        # TODO: Delegate to RegimeTrainer and store fitted models
        # from regime.trainer import RegimeTrainer
        # trainer = RegimeTrainer()
        # features = trainer.prepare_features(df)
        # self.hmm_model = trainer.train_hmm(features)
        # hmm_states = self.hmm_model.predict(features)
        # self.svm_model = trainer.train_svm(features, hmm_states)
        # logger.info("RegimeDetector training complete.")
        logger.warning("train() not yet implemented.")

    # ------------------------------------------------------------------
    def predict(self, df: pd.DataFrame) -> str:
        """Predict the current market regime for the latest data.

        Args:
            df: Recent OHLCV DataFrame (at minimum the last few hundred bars).

        Returns:
            One of ``TRENDING``, ``MEAN_REVERTING``, or ``BREAKOUT``.
        """
        # TODO: Extract features, run through SVM, return regime label
        # from regime.trainer import RegimeTrainer
        # trainer = RegimeTrainer()
        # features = trainer.prepare_features(df)
        # latest_features = features.iloc[[-1]]
        # regime_label = self.svm_model.predict(latest_features)[0]
        # logger.debug(f"Predicted regime: {regime_label}")
        # return regime_label
        logger.warning("predict() not yet implemented.")
        return TRENDING

    # ------------------------------------------------------------------
    def confirm_regime(
        self,
        regime_history: list[str] | deque[str],
        n: int = 3,
    ) -> str | None:
        """Confirm a regime change only after N consecutive identical labels.

        Guards against spurious regime flips caused by noisy model output.

        Args:
            regime_history: Ordered list of recent regime labels (latest last).
            n: Number of consecutive identical labels required to confirm.

        Returns:
            The confirmed regime label if the last ``n`` labels agree,
            otherwise ``None`` (no confirmed change yet).
        """
        # TODO: Implement confirmation logic
        # if len(regime_history) < n:
        #     return None
        # recent = list(regime_history)[-n:]
        # if len(set(recent)) == 1:
        #     confirmed = recent[0]
        #     logger.info(f"Regime confirmed: {confirmed} ({n} consecutive candles).")
        #     return confirmed
        # return None
        logger.warning("confirm_regime() not yet implemented.")
        return None
