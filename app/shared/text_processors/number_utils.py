# Utilidades para convertir números y patrones simples a texto en español.
# Este módulo utiliza `num2words` si está disponible. Para instalarlo: pip install num2words

from __future__ import annotations

import re
from typing import Optional

try:
    from num2words import num2words  # type: ignore
except Exception:
    num2words = None

_RE_INT = re.compile(r"(?<!\d)(\d{1,15})(?!\d)")
_RE_DEC_COMMA = re.compile(r"(?<!\d)(\d+[.,]\d+)(?!\d)")
_RE_PERCENT = re.compile(r"(?<!\d)(\d+[.,]?\d*)%")
_RE_PHONE = re.compile(r"\b(\+?\d[\d\s\-]{5,}\d)\b")


class NumberConverter:
    # Convertidor que transforma patrones numéricos en palabras en español.
    # Prioriza `num2words` cuando está disponible para una cobertura lingüística completa.

    def __init__(self, lang: str = "es"):
        self.lang = lang

    def int_to_text(self, value: int) -> str:
        if num2words:
            return num2words(value, lang=self.lang)
        return self._simple_int_to_text(value)

    def decimal_to_text(self, value: str, decimal_sep: str = ".") -> str:
        # value like '6.9' or '11,0'
        if num2words:
            # normalize to dot for num2words
            normalized = value.replace(",", ".")
            if "." in normalized:
                whole, frac = normalized.split(".", 1)
                w = num2words(int(whole), lang=self.lang)
                f = " ".join(num2words(int(d), lang=self.lang) for d in frac)
                # keep separators explicit
                sep_word = "coma" if "," in value or decimal_sep == "," else "punto"
                return f"{w} {sep_word} {f}"
            return num2words(int(normalized), lang=self.lang)

        # fallback: simple handling
        if "," in value:
            whole, frac = value.split(",", 1)
            sep_word = "coma"
        else:
            whole, frac = value.split(".", 1)
            sep_word = "punto"

        return f"{self._simple_int_to_text(int(whole))} {sep_word} {' '.join(self._simple_int_to_text(int(d)) for d in frac)}"

    def percent_to_text(self, value: str) -> str:
        # value like '11,0%'
        m = _RE_PERCENT.match(value)
        if not m:
            return value
        num = m.group(1)
        # preserve decimal handling
        if "," in num or "." in num:
            text = self.decimal_to_text(num, decimal_sep="," if "," in num else ".")
        else:
            text = self.int_to_text(int(num))
        return f"{text} por ciento"

    def phone_to_text(self, value: str) -> str:
        # Expand phone digits with spaces between numbers
        digits = re.sub(r"\D+", "", value)
        return " ".join(self._digit_to_word(d) for d in digits)

    def _digit_to_word(self, d: str) -> str:
        mapping = {
            "0": "cero",
            "1": "uno",
            "2": "dos",
            "3": "tres",
            "4": "cuatro",
            "5": "cinco",
            "6": "seis",
            "7": "siete",
            "8": "ocho",
            "9": "nueve",
        }
        return mapping.get(d, d)

    def _simple_int_to_text(self, value: int) -> str:
        # Very small fallback converter for non num2words environments.
        units = [
            "cero",
            "uno",
            "dos",
            "tres",
            "cuatro",
            "cinco",
            "seis",
            "siete",
            "ocho",
            "nueve",
            "diez",
            "once",
            "doce",
            "trece",
            "catorce",
            "quince",
            "dieciseis",
            "diecisiete",
            "dieciocho",
            "diecinueve",
        ]
        tens = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]

        if value < len(units):
            return units[value]
        if value < 100:
            t = value // 10
            u = value % 10
            if t == 2 and u != 0:
                return f"veinti{units[u]}"
            if u == 0:
                return tens[t]
            return f"{tens[t]} y {units[u]}"
        if value < 1000:
            hundreds = value // 100
            remainder = value % 100
            if value == 100:
                return "cien"
            prefix = "ciento" if hundreds == 1 else {
                2: "doscientos",
                3: "trescientos",
                4: "cuatrocientos",
                5: "quinientos",
                6: "seiscientos",
                7: "setecientos",
                8: "ochocientos",
                9: "novecientos",
            }[hundreds]
            if remainder == 0:
                return prefix
            return f"{prefix} {self._simple_int_to_text(remainder)}"
        if value < 10000:
            thousands = value // 1000
            remainder = value % 1000
            prefix = "mil" if thousands == 1 else f"{self._simple_int_to_text(thousands)} mil"
            if remainder == 0:
                return prefix
            return f"{prefix} {self._simple_int_to_text(remainder)}"
        # fallback for larger numbers: return digits joined
        return " ".join(self._digit_to_word(d) for d in str(value))

    def replace_numbers_in_text(self, text: str) -> str:
        """
        Reemplaza números, porcentajes y fonemas en el texto de entrada con palabras en español.
        Esta función está optimizada para la transmisión de datos: aplica expresiones regulares sencillas y
        utiliza num2words cuando está disponible.
        """

        # percentages first
        def _p(m: re.Match) -> str:
            return self.percent_to_text(m.group(0))

        text = _RE_PERCENT.sub(_p, text)

        # decimals
        def _d(m: re.Match) -> str:
            return self.decimal_to_text(m.group(1))

        text = _RE_DEC_COMMA.sub(lambda m: _d(m), text)

        # integers
        text = _RE_INT.sub(lambda m: self.int_to_text(int(m.group(1))), text)

        # phones
        text = _RE_PHONE.sub(lambda m: self.phone_to_text(m.group(1)), text)

        return text


__all__ = ["NumberConverter"]
