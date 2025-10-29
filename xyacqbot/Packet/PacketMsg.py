import warnings
from dataclasses import dataclass, field
from typing import List, Optional, Union, Literal, Dict, Any
from .PacketBase import PacketBase
from ..datamanager.GlobleDataManager import GlobalDataManager


# -------------------- 基础消息段定义 --------------------

@dataclass
class TextSegment:
    type: Literal["text"]
    data: Dict[str, str]

    def getText(self) -> str:
        return self.data.get("text", "")


@dataclass
class VideoSegment:
    type: Literal["video"]
    data: Dict[str, Any]

    def getFileName(self) -> str:
        return self.data.get("file", "")

    def getUrl(self) -> str:
        return self.data.get("url", "")

    def getPath(self) -> str:
        return self.data.get("path", "")

    def getSize(self) -> str:
        return self.data.get("file_size", "")


@dataclass
class RecordSegment:
    type: Literal["record"]
    data: Dict[str, Any]

    def getFileName(self) -> str:
        return self.data.get("file", "")

    def getUrl(self) -> str:
        return self.data.get("url", "")

    def getPath(self) -> str:
        return self.data.get("path", "")

    def getSize(self) -> str:
        return self.data.get("file_size", "")


@dataclass
class FileSegment:
    type: Literal["file"]
    data: Dict[str, Any]

    def getFileName(self) -> str:
        return self.data.get("file", "")

    def getUrl(self) -> str:
        return self.data.get("url", "")

    def getFileId(self) -> str:
        return self.data.get("file_id", "")

    def getPath(self) -> str:
        return self.data.get("path", "")

    def getSize(self) -> str:
        return self.data.get("file_size", "")


@dataclass
class AtSegment:
    type: Literal["at"]
    data: Dict[str, Any]

    def getName(self) -> str:
        return self.data.get("name", "")

    def getId(self) -> str:
        return self.data.get("qq", 0)


@dataclass
class ReplySegment:
    type: Literal["reply"]
    data: Dict[str, Any]

    def getId(self) -> str:
        return self.data.get("id", 0)


@dataclass
class ImageSegment:
    type: Literal["image"]
    data: Dict[str, Any]

    def getFileName(self) -> str:
        return self.data.get("file", "")

    def getSubType(self) -> str:
        return self.data.get("sub_type", "")

    def getUrl(self) -> str:
        return self.data.get("url", "")

    def getSize(self) -> str:
        return self.data.get("file_size", "")


MessageSegment = Union[
    TextSegment,
    VideoSegment,
    RecordSegment,
    FileSegment,
    AtSegment,
    ReplySegment,
    ImageSegment,
    Dict[str, Any]  # 兜底以防有其他段未定义
]


@dataclass
class Sender:
    user_id: int
    nickname: str
    card: Optional[str] = None
    sex: Optional[Literal["male", "female", "unknown"]] = None
    age: Optional[int] = None
    level: Optional[str] = None
    role: Optional[Literal["owner", "admin", "member"]] = None
    title: Optional[str] = None
    group_id: Optional[int] = None


class PacketMsg(PacketBase):
    time: int
    self_id: int
    post_type: Literal["message", "message_sent"]
    message_id: int
    message_seq: int
    real_id: Optional[int]
    user_id: int
    group_id: Optional[int]
    message_type: Literal["private", "group"]
    sub_type: Optional[str]
    sender: Sender
    message: List[MessageSegment]
    message_format: Literal["array", "string"]
    raw_message: str
    font: int
    target_id: Optional[int] = None
    temp_source: Optional[int] = None

    @staticmethod
    def like(packet_data: dict) -> bool:
        return "message_type" in packet_data

    def __init__(self,  packet_data: dict):
        super().__init__(packet_data)
        # 将 dict 自动解析成 dataclass
        self.time = packet_data.get("time")
        self.self_id = packet_data.get("self_id")
        self.post_type = packet_data.get("post_type")
        self.message_id = packet_data.get("message_id")
        self.message_seq = packet_data.get("message_seq")
        self.real_id = packet_data.get("real_id")
        self.user_id = packet_data.get("user_id")
        self.group_id = packet_data.get("group_id")
        self.message_type = packet_data.get("message_type")
        self.sub_type = packet_data.get("sub_type")
        self.sender = Sender(**packet_data["sender"])
        self.message = [self._parseMessageSegment(
            seg) for seg in packet_data["message"]]
        self.message_format = packet_data.get("message_format")
        self.raw_message = packet_data.get("raw_message")
        self.font = packet_data.get("font", 14)
        self.target_id = packet_data.get("target_id")
        self.temp_source = packet_data.get("temp_source")

    def _parseMessageSegment(self, seg: dict) -> MessageSegment:
        seg_type = seg.get("type")
        if seg_type == "text":
            return TextSegment(**seg)
        elif seg_type == "video":
            return VideoSegment(**seg)
        elif seg_type == "record":
            return RecordSegment(**seg)
        elif seg_type == "file":
            return FileSegment(**seg)
        elif seg_type == "at":
            return AtSegment(**seg)
        elif seg_type == "reply":
            return ReplySegment(**seg)
        elif seg_type == "image":
            return ImageSegment(**seg)
        return seg  # 未定义类型直接返回 dict

    def shouldIgnore(self) -> bool:
        global_data = GlobalDataManager()
        if str(self.group_id) in global_data.getEnbaleGroupList():
            return False
        return True

    def getNickname(self) -> str:
        return self.sender.nickname

    def getCardname(self) -> str:
        return self.sender.card

    def getName(self) -> str:
        name = self.getCardname()
        if name == "":
            name = self.getNickname()
        return name

    def checkOwner(self) -> bool:
        return self.sender.role == "owner"

    def checkAdmin(self) -> bool:
        return self.sender.role == "admin"

    def checkOwnerOrAdmin(self) -> bool:
        return self.checkOwner() or self.checkAdmin()

    def getId(self) -> int:
        return self.sender.user_id

    def getMsg(self) -> str:
        return self.raw_message
