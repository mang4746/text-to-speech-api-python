import re
from typing import List


class TextStreamBuffer:
    """Buffer de texto incremental que detecta frases listas para sintetizar."""

    _phrase_pattern = re.compile(r"(.+?[\.,;:!\?]+)(?:\s+|$)", re.UNICODE)

    def __init__(self, max_buffer_chars: int = 240):
        self._buffer: str = ""
        self.max_buffer_chars = max_buffer_chars

    def append_text(self, text: str) -> List[str]:
        """Agrega texto al buffer y retorna frases listas para generar audio."""
        # Añadir fragmento tal cual; no hacer strip aquí para preservar espacios
        # que pueden ser parte del stream letra-a-letra.
        self._buffer += text
        ready_phrases: List[str] = []

        while True:
            match = self._phrase_pattern.match(self._buffer)
            if not match:
                break
            # Extraer la frase y normalizar espacios alrededor
            phrase = match.group(1).strip()
            if phrase:
                ready_phrases.append(phrase)
            # Mantener el resto del buffer tal cual (no eliminar espacios a la izquierda)
            self._buffer = self._buffer[match.end():]

        if len(self._buffer) > self.max_buffer_chars:
            split_pos = self._buffer.rfind(" ", 0, self.max_buffer_chars)
            if split_pos <= 0:
                split_pos = self.max_buffer_chars
            phrase = self._buffer[:split_pos].strip()
            self._buffer = self._buffer[split_pos:]
            if phrase:
                ready_phrases.append(phrase)

        return ready_phrases

    def flush(self) -> List[str]:
        """Devuelve el texto restante en el buffer y lo vacía."""
        # Normalizar espacios múltiples a uno y limpiar bordes
        pending = re.sub(r"\s+", " ", self._buffer).strip()
        self._buffer = ""
        return [pending] if pending else []

    @property
    def pending_text(self) -> str:
        # Mostrar el texto pendiente normalizando secuencias de espacios
        return re.sub(r"\s+", " ", self._buffer).strip()

    def is_empty(self) -> bool:
        return not bool(re.sub(r"\s+", " ", self._buffer).strip())
