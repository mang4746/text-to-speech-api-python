from typing import Any


def build_response(status: str, message: str, data: Any = None) -> dict:
    return {"status": status, "message": message, "data": data}
