"""Módulo de voz por streaming."""
from fastapi import APIRouter

from .router import router

__all__ = ["router"]
