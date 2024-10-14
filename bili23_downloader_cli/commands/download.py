from typing import Annotated
from typer import Option, Typer
from rich.panel import Panel
from rich.console import group
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Static, Button
from rich.console import ConsoleRenderable, RichCast

download = Typer(no_args_is_help=True)


class ItemLabel(Static):
    """视频名称"""


class Item(Static):
    """每一个下载的item"""

    def __init__(
        self,
        renderable: ConsoleRenderable | RichCast | str = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self.init_styles()
        super().__init__(
            renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield ItemLabel("视频名称")

    def init_styles(self):
        self.styles.layout = "horizontal"
        self.styles.height = 5


class DownloadManager(App):  # type: ignore
    CSS_PATH = "../static/css/download.tcss"
    BINDINGS = [("d", "toggle_dd", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(Item())

    def action_toggle_dd(self) -> None:
        self.dark = not self.dark


@download.command(
    "list",
)
def list_downloading_videos():
    """显示下载中的视频"""
    donwload_manager = DownloadManager()
    donwload_manager.run()


@group()
def get_downloading_videos():
    """获取下载中的视频列表"""
    for i in range(0, 5):
        yield Panel(f"video: 第{i} 个视频")


@download.callback()
def main(
    # url: Annotated[
    #     str,
    #     Argument(default=None, help="视频链接,暂不支持输入多个url地址", show_default=False),
    # ] = None,
    show_info: Annotated[
        bool, Option("--info", "-i")
    ] = False,  # 下载的时候默认不显示视频的信息，如果需要显示，则跟 --info / -i
):
    """下载/管理视频"""

    # video_info = get_video_info(url)
    # get_video_type(video_info["type"])

    if show_info:
        # TODO： 需要接rich 打印视频的信息
        ...

    # TODO: 这里可以跟上promt 进行交互
    # 是否选择 视频品质，默认为配置的value
    # 是否选择 音频品质, 同上
    # ...
