"""
定义常量的文件
"""

from enum import Enum


quality_map = {
    "超高清 8K": 127,
    "杜比视界": 126,
    "真彩 HDR": 125,
    "超清 4K": 120,
    "高清 1080P60": 116,
    "高清 1080P+": 112,
    "高清 1080P": 80,
    "高清 720P": 64,
    "清晰 480P": 32,
    "流畅 360P": 16,
}
codec_map = {"AVC/H.264": "avc", "HEVC/H.265": "hevc", "AV1": "av1"}


class VideoQuality(Enum):
    """视频品质"""

    UHD_8K = ("超高清 8K", 127)
    """超高清 8K"""
    DOLBY = ("杜比视界", 126)
    """杜比视界"""
    HDR = ("真彩 HDR", 125)
    """真彩 HDR"""
    UHD_4K = ("超清 4K", 120)
    """超清 4K"""
    HD_1080P60 = ("高清 1080P60", 116)
    """高清 1080P60"""
    HD_1080Plus = ("高清 1080P+", 112)
    """高清 1080P+"""
    HD_1080P = ("高清 1080P", 80)
    """高清 1080P"""
    HD_720P = ("高清 720P", 64)
    """高清 720P"""
    CLEAR = ("清晰 480P", 32)
    """清晰 480P"""
    SMOOTH = ("流畅 360P", 16)
    """流畅 360P"""


class VideoCodec(Enum):
    """视频编解码"""

    AVC = ("AVC/H.264", "avc")
    HEVC = ("HEVC/H.265", "hevc")
    AV1 = ("AV1", "av1")
