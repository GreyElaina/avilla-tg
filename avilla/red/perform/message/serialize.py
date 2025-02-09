from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from avilla.core.elements import Notice, NoticeAll, Picture, Text, Emoji, Audio
from avilla.core.ryanvk.collector.account import AccountCollector
from avilla.core.ryanvk.descriptor.message.serialize import MessageSerialize
from avilla.standard.qq.elements import MarketFace

if TYPE_CHECKING:
    from avilla.red.account import RedAccount  # noqa
    from avilla.red.protocol import RedProtocol  # noqa

RedMessageSerialize = MessageSerialize[dict]


class RedMessageSerializePerform((m := AccountCollector["RedProtocol", "RedAccount"]())._):
    m.post_applying = True

    # LINK: https://github.com/microsoft/pyright/issues/5409

    @RedMessageSerialize.collect(m, Text)
    async def text(self, element: Text) -> dict:
        return {"elementType": 1, "textElement": {"content": element.text}}

    @RedMessageSerialize.collect(m, Emoji)
    async def face(self, element: Emoji) -> dict:
        return {"elementType": 6, "faceElement": {"faceIndex": element.id}}

    @RedMessageSerialize.collect(m, Notice)
    async def notice(self, element: Notice) -> dict:
        return {"elementType": 1, "textElement": {"atType": 2, "atNtUin": element.target.last_value}}

    @RedMessageSerialize.collect(m, NoticeAll)
    async def notice_all(self, element: NoticeAll) -> dict:
        return {"elementType": 1, "textElement": {"atType": 1}}

    @RedMessageSerialize.collect(m, Picture)
    async def picture(self, element: Picture) -> dict:
        data = await self.account.staff.fetch_resource(element.resource)
        resp = await self.account.websocket_client.call_http(
            "multipart",
            "api/upload",
            {
                "file": {
                    "value": data,
                    "content_type": None,
                    "filename": "file_image",
                }
            },
        )
        file = Path(resp["ntFilePath"])
        return {
            "elementType": 2,
            "picElement": {
                "original": True,
                "md5HexStr": resp["md5"],
                "picWidth": resp["imageInfo"]["width"],
                "picHeight": resp["imageInfo"]["height"],
                "fileSize": resp["fileSize"],
                "fileName": file.name,
                "sourcePath": resp["ntFilePath"],
            },
        }

    @RedMessageSerialize.collect(m, MarketFace)
    async def market_face(self, element: MarketFace) -> dict:
        emoji_id, key, emoji_package_id = element.id.split("/")
        return {
            "elementType": 11,
            "marketFaceElement": {
                "emojiId": int(emoji_id),
                "key": key,
                "emojiPackageId": int(emoji_package_id),
            },
        }

    @RedMessageSerialize.collect(m, Audio)
    async def audio(self, element: Audio) -> dict:
        data = await self.account.staff.fetch_resource(element.resource)
        resp = await self.account.websocket_client.call_http(
            "multipart",
            "api/upload",
            {
                "file": {
                    "value": data,
                    "content_type": None,
                    "filename": "file_audio",
                }
            },
        )
        file = Path(resp["ntFilePath"])
        return {
            "elementType": 4,
            "pttElement": {
                "canConvert2Text": True,
                "md5HexStr": resp.md5,
                "fileSize": resp.fileSize,
                "fileName": file.name,
                "filePath": resp.ntFilePath,
                "duration": 1,
                "formatType": 1,
                "voiceType": 1,
                "voiceChangeType": 0,
                "playState": 1,
                "waveAmplitudes": [99 for _ in range(17)]
            },
        }
