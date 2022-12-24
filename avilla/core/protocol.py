from __future__ import annotations

from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, ClassVar

from avilla.core._runtime import ctx_avilla, ctx_protocol, ctx_context
from avilla.core.account import AbstractAccount
from avilla.core.event import AvillaEvent
from avilla.core.trait.context import Artifacts
from avilla.core.platform import Abstract, Land, Platform
from avilla.core.utilles.selector import Selector

if TYPE_CHECKING:
    from avilla.core.application import Avilla
    from avilla.core.context import Context


@contextmanager
def _empty_ctxmgr():
    yield


class BaseProtocol(metaclass=ABCMeta):
    avilla: Avilla
    platform: ClassVar[Platform]

    implementations: ClassVar[Artifacts]

    def __init__(self):
        ...

    @property
    def land(self):
        return self.platform[Land]

    @property
    def abstract(self):
        return self.platform[Abstract]

    @abstractmethod
    def ensure(self, avilla: Avilla) -> Any:
        ...

    def get_accounts(self, selector: Selector | None = None) -> list[AbstractAccount]:
        return self.avilla.get_accounts(selector=selector, land=self.platform[Land])

    def get_account(self, selector: Selector) -> AbstractAccount | None:
        return self.avilla.get_account(selector=selector, land=self.platform[Land])

    def post_event(self, event: AvillaEvent, context: Context | None = None):
        with ctx_avilla.use(self.avilla), ctx_protocol.use(self), (
            ctx_context.use(context) if context is not None else _empty_ctxmgr()
        ):
            return self.avilla.broadcast.postEvent(event)
