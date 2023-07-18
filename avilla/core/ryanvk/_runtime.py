from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .isolate import Isolate

processing_isolate: ContextVar[Isolate] = ContextVar("processing_isolate")
