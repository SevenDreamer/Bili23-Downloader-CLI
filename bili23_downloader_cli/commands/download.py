from typing import Annotated
from typer import Argument, Option, Typer

download = Typer()


@download.command("list")
def list_download():
    """显示下载列表"""


@download.callback()
def main(
    url: Annotated[
        str | None,
        Argument(help="视频链接,暂不支持输入多个url地址", show_default=False),
    ] = None,
    show_info: Annotated[
        bool, Option("--info", "-i")
    ] = False,  # 下载的时候默认不显示视频的信息，如果需要显示，则跟 --info / -i
):
    """下载"""

    # video_info = get_video_info(url)
    # get_video_type(video_info["type"])

    if show_info:
        # TODO： 需要接rich 打印视频的信息
        ...

    # TODO: 这里可以跟上promt 进行交互
    # 是否选择 视频品质，默认为配置的value
    # 是否选择 音频品质, 同上
    # ...
