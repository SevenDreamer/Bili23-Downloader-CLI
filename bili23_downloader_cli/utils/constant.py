"""
定义常量的文件
"""

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


# class Quality(Enum):
#     "超高清 8K"= 127
#     "杜比视界"= 126
#     "真彩 HDR"= 125
#     "超清 4K"= 120
#     "高清 1080P60"= 116
#     "高清 1080P+"= 112
#     "高清 1080P"= 80
#     "高清 720P"= 64
#     "清晰 480P"= 32
#     "流畅 360P"= 16
