from datetime import datetime
from telethon import Button
from telethon.types import TypeInputFile
from typing import Any, List, Literal, Optional, TypedDict

# Extra classes since python is stupid
class APIAttachmentContent(TypedDict):
    data: bytes

class APIEmbedField(TypedDict):
    name: str
    value: str
    inline: Optional[bool]

class APIEmbedAuthor(TypedDict):
    name: Optional[str]
    iconURL: Optional[str]

class APIEmbedFooter(TypedDict):
    text: Optional[str]
#

class APIAttachment(TypedDict):
    content: APIAttachmentContent
    name: Optional[str]

class APIEmbed(TypedDict):
    title: Optional[str]
    fields: List[APIEmbedField]
    description: Optional[str]
    author: Optional[APIEmbedAuthor]
    footer: Optional[APIEmbedFooter]
    image: Optional[str]
    thumbnail: Optional[str]
    timestamp: Optional[datetime]
    color: str

class APIButton(TypedDict):
    id: str
    label: str
    style: Literal['Primary'] | Literal['Secondary'] | Literal['Success'] | Literal['Danger'] | Literal['Link']
    disabled: Optional[bool]
class APISelect(TypedDict):
    value: str
    label: str
    description: str
    enabled: Optional[bool]
class APISelectMenu(TypedDict):
    id: str
    placeholder: str
    options: List[APISelect]
    min: int
    max: int

class APICommandResponse(TypedDict):
    embeds: List[APIEmbed]
    files: List[APIAttachment]
    buttons: List[List[APIButton]]
    menus: List[APISelectMenu]
    content: Optional[str]

class WSTelegramResponse(TypedDict):
    event: Literal['spawn'] | Literal['levelup'] | Literal['dm'] | Literal['reply']
    chatID: Optional[str] # Only for 'spawn', 'levelup', 'dm'
    payloadID: Optional[str] # Only for 'reply'
    embeds: List[APIEmbed]
    files: List[APIAttachment]
    buttons: List[List[APIButton]]
    menus: List[APISelectMenu]
    content: Optional[str]

class WSInvalidResponse(TypedDict):
    event: Literal['reply']
    status: int
    payloadID: str

class APITelegramPayload(TypedDict):
    platform: Literal['telegram']
    values: Optional[str]
    userID: str
    userName: str
    chatID: str
    timestamp: int
    extra: Optional[Any]

class WSTelegramSend(TypedDict):
    platform: Literal['telegram']
    event: Literal['send']
    userID: str
    userName: str
    chatID: str

class WSTelegramChats(TypedDict):
    platform: Literal['telegram']
    event: Literal['added'] | Literal['removed']
    id: str
    name: str
    total: int

class WSTelegramCommand(APITelegramPayload):
    event: Literal['command']
    command: str
    payloadID: str

class WSTelegramCallback(APITelegramPayload):
    event: Literal['callback']
    callback: str
    payloadID: str

WSTelegramPayload = (
    WSTelegramSend
    | WSTelegramChats
    | WSTelegramCommand
    | WSTelegramCallback
)

class CommandResponse(TypedDict):
    content: str
    files: List[TypeInputFile]
    buttons: List[List[Button]]
    menus: List[APISelectMenu]
