from __future__ import annotations

from typing import TYPE_CHECKING

from nonechat.info import Event
from nonechat.message import Element

from avilla.core.account import AccountStatus, BaseAccount
from avilla.core.platform import Abstract, Land, Platform
from avilla.core.selector import Selector

if TYPE_CHECKING:
    from .protocol import ConsoleProtocol

PLATFORM = Platform(
    Land(
        "console",
        [{"name": "GraiaxCommunity"}],
        humanized_name="Avilla-Console - Console Impl for avilla",
    ),
    Abstract(
        protocol="Console",
        maintainers=[{"name": "yanyongyu"}],
        humanized_name="Textual Console",
    ),
)


class ConsoleAccount(BaseAccount):
    protocol: ConsoleProtocol
    status: AccountStatus

    def __init__(self, protocol: ConsoleProtocol):
        super().__init__(Selector().land("console").account(protocol.name), protocol.avilla)
        self.protocol = protocol
        self.status = AccountStatus()

    @property
    def client(self):
        return self.protocol.service.app

    @property
    def available(self) -> bool:
        return self.status.enabled

    def __staff_generic__(self, element_type: Element, event_type: Event):
        ...
