# Proceso de preprocesamiento de texto TTS.
# Diseñado para ser reutilizable, extensible y eficiente en streaming.

from __future__ import annotations

import html
import re
from enum import Enum
from typing import Callable, List, Literal, Optional

from .number_utils import NumberConverter

# Precompiled regexes for performance
_EMOJI_RE = re.compile(
    "([\U0001F1E0-\U0001F6FF]|[\u2600-\u26FF]|[\u2700-\u27BF]|[\U0001F900-\U0001F9FF])",
    flags=re.UNICODE,
)

# URLs: captura http(s):// o www. seguido de no-espacios; la puntuación final se limpia en _format_url_verbose
_URL_RE = re.compile(r"https?://[^\s]+|www\.[^\s]+")
_MARKDOWN_RE = re.compile(r"\*\*(.*?)\*\*|\*(.*?)\*|`([^`]+)`|\[(.*?)\]\((.*?)\)")
_MD_HEADING_RE = re.compile(r"^#{1,6}\s+", flags=re.MULTILINE)
_HASH_RE = re.compile(r"#+")
_WEIRD_CHARS_RE = re.compile(r"[^\S\r\n]+")
_MULTI_NEWLINE_RE = re.compile(r"\n{2,}")
_CAMEL_BOUNDARY_RE = re.compile(r"(?<=[a-záéíóúñü])(?=[A-ZÁÉÍÓÚÑÜ])")
_TEMPERATURE_RE = re.compile(r"°\s*C\b", flags=re.IGNORECASE)
_STREET_NUMBER_RE = re.compile(r"[Nn]°\s*", flags=re.IGNORECASE)


class UrlMode(str, Enum):
    LITERAL = "literal"
    VERBOSE = "verbose"


class Rule:
    def __init__(self, name: str, func: Callable[[str], str]):
        self.name = name
        self.func = func

    def apply(self, text: str) -> str:
        return self.func(text)


class TextPreprocessor:
    """Pipeline de preprocesado de texto para TTS.

    Uso:
        pre = TextPreprocessor()
        out = pre.preprocess(text)

    Soporta `append_fragment` para textos fragmentados en streaming.
    """

    def __init__(
        self,
        number_converter: Optional[NumberConverter] = None,
        url_mode: Literal[UrlMode.LITERAL, UrlMode.VERBOSE] = UrlMode.VERBOSE,
    ):
        self.number_converter = number_converter or NumberConverter()
        self.url_mode = url_mode
        self._rules: List[Rule] = [
            Rule("unescape_html", self._unescape_html),
            Rule("remove_emojis", self._remove_emojis),
            Rule("remove_md_headings", self._remove_md_headings),
            Rule("remove_hashes", self._remove_hashes),
            Rule("strip_markdown", self._strip_markdown),
            Rule("normalize_urls", self._normalize_urls),
            Rule("replace_temperature_units", self._replace_temperature_units),
            Rule("replace_street_numbers", self._replace_street_numbers),
            Rule("separate_camel_case", self._separate_camel_case),
            Rule("cleanup_weird_chars", self._cleanup_weird_chars),
            Rule("normalize_spaces", self._normalize_spaces),
            Rule("normalize_newlines", self._normalize_newlines),
            Rule("numbers_to_text", self._numbers_to_text),
        ]

        # buffer for streaming fragments (minimal state)
        self._fragment_buffer: List[str] = []

    def register_rule(self, rule: Rule, position: Optional[int] = None) -> None:
        if position is None:
            self._rules.append(rule)
        else:
            self._rules.insert(position, rule)

    def preprocess(self, text: str) -> str:
        s = text
        for rule in self._rules:
            s = rule.apply(s)
        return s.strip()

    def append_fragment(self, fragment: str) -> str:
        """
        Añade un fragmento de transmisión y devuelve la salida procesada para dicho 
        La implementación mantiene un pequeño búfer para evitar la división de tokens entre fragmentos.
        """
        # Keep small buffer length to minimize memory.
        self._fragment_buffer.append(fragment)
        if len(self._fragment_buffer) > 5:
            # drop oldest if too many fragments accumulated
            self._fragment_buffer.pop(0)

        joined = "".join(self._fragment_buffer)

        # Heuristic: only process when a sentence terminator or newline present
        if any(c in joined for c in ".!?\n"):
            out = self.preprocess(joined)
            # clear buffer after emitting processed text
            self._fragment_buffer.clear()
            return out

        # otherwise return empty and wait for more fragments
        return ""

    # ---- Rule implementations ----
    def _unescape_html(self, text: str) -> str:
        return html.unescape(text)

    def _remove_emojis(self, text: str) -> str:
        # remove common emoji ranges; keep simple and fast
        return _EMOJI_RE.sub(" ", text)

    def _strip_markdown(self, text: str) -> str:
        return _MARKDOWN_RE.sub(lambda m: next((g for g in m.groups() if g), ""), text)

    def _remove_md_headings(self, text: str) -> str:
        # Reemplaza encabezados tipo "### Texto" por un espacio (evita que TTS lea los hashes)
        return _MD_HEADING_RE.sub(" ", text)

    def _remove_hashes(self, text: str) -> str:
        # Elimina cualquier símbolo de numeral "#" que aparezca en el texto.
        return _HASH_RE.sub(" ", text)

    def _separate_camel_case(self, text: str) -> str:
        # Inserta espacio entre minúscula seguida de mayúscula para mejorar la lectura TTS.
        # Ej: 'PatacamayaClaro' -> 'Patacamaya Claro'
        return _CAMEL_BOUNDARY_RE.sub(" ", text)

    def _normalize_urls(self, text: str) -> str:
        # Aplicar ANTES que _numbers_to_text para evitar procesar tokens ilegibles
        if self.url_mode == UrlMode.LITERAL:
            return text

        return _URL_RE.sub(lambda m: self._format_url_verbose(m.group(0)), text)

    def _replace_temperature_units(self, text: str) -> str:
        # Convierte °C a 'grados' para que el TTS use lenguaje natural.
        return _TEMPERATURE_RE.sub("grados", text)

    def _replace_street_numbers(self, text: str) -> str:
        # Convierte N° a 'número' para direcciones callejeras.
        # Ej: 'Calle Franco N° 49' -> 'Calle Franco número 49'
        return _STREET_NUMBER_RE.sub("número ", text)

    def _is_suspicious_segment(self, segment: str) -> bool:
        # Detecta si un segmento de URL es ilegible (token, hash, código aleatorio).

        # 1. URL-encoded characters
        if '%' in segment:
            return True
        
        # 2. Caracteres especiales sospechosos
        if any(c in segment for c in '$@&=!*+~^'):
            return True
        
        # 3. Mezcla de letras + números (ej: FQe6LFU, abc123, Test99)
        # Si tiene dígitos y al menos una letra, es probable que sea un hash/token
        has_upper = any(c.isupper() for c in segment)
        has_lower = any(c.islower() for c in segment)
        has_digit = any(c.isdigit() for c in segment)
        if has_digit and (has_upper or has_lower):
            return True
        
        # 4. Muy largo (probable token/hash)
        if len(segment) > 15:
            return True
        
        return False

    def _format_url_verbose(self, url: str) -> str:
        # Formatea URL para TTS legible: 'https://ejemplo.com/docs' -> 'ejemplo punto com barra docs'

        # Limpia puntuación final que puede estar en la URL por ser parte de una oración
        url = re.sub(r'[,;:.!?\)]+$', '', url)
        
        # Quita protocolo https:// o http://
        cleaned = re.sub(r"^https?://", "", url, flags=re.IGNORECASE)
        # Quita trailing slashes
        cleaned = cleaned.rstrip("/")
        
        # Separa host y path
        parts = cleaned.split("/", 1)
        host = parts[0]
        path = parts[1] if len(parts) > 1 else ""
        
        # Convierte host: bdp.com.bo -> bdp punto com punto bo
        host_text = " punto ".join(host.split("."))
        if not path:
            return host_text
        
        # Quita query strings (?...) y fragmentos (#...)
        path = re.split(r"[?#]", path, 1)[0]
        
        # Filtra segmentos sospechosos (tokens, hashes, códigos URL-encoded)
        segments = []
        for seg in path.split("/"):
            if seg and not self._is_suspicious_segment(seg):
                segments.append(seg)
        
        # Si no hay segmentos válidos, solo devuelve el host
        if not segments:
            return host_text
        
        # Convierte path: productos/credito -> barra productos barra credito
        return f"{host_text} barra {' barra '.join(segments)}"

    def _cleanup_weird_chars(self, text: str) -> str:
        # remove multiple non-space control characters, preserve newlines
        # Also remove uncommon unicode control chars
        return re.sub(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]+", " ", text)

    def _normalize_spaces(self, text: str) -> str:
        # collapse horizontal whitespace to single spaces
        return _WEIRD_CHARS_RE.sub(" ", text)

    def _normalize_newlines(self, text: str) -> str:
        # collapse multiple newlines, keep single as sentence separators
        return _MULTI_NEWLINE_RE.sub("\n", text).strip()

    def _numbers_to_text(self, text: str) -> str:
        # Delegate to NumberConverter. This function tries to avoid heavy regex loops.
        return self.number_converter.replace_numbers_in_text(text)


__all__ = ["TextPreprocessor", "Rule", "UrlMode"]
