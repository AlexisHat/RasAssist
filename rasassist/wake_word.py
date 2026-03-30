import numpy as np
import openwakeword


class WakeWordDetector:
    """Erkennt ein Wake-Word in einem eingehenden Audio-Chunk."""

    def __init__(self, model_path: str, threshold: float = 0.20):
        self.threshold = threshold
        self._model = openwakeword.Model(wakeword_models=[model_path])

    def predict(self, audio_chunk: bytes) -> bool:
        """Gibt True zurück, wenn das Wake-Word im Chunk erkannt wurde."""
        frame = np.frombuffer(audio_chunk, dtype=np.int16)
        scores = self._model.predict(frame)
        return any(score > self.threshold for score in scores.values())
