from enum import Enum
import time
from typing import Annotated, Any, Dict

from typer import Option, Typer
from rich import print
from qrcode import QRCode

from bili23_downloader_cli.config import check_config, save_config
from bili23_downloader_cli.api import Api, LoginQRCodeInfo

app = Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Bilibili视频下载器",
    epilog="Made with :heart:  in [blue]Seven Dreamer[/blue]",
)


class VideoType(Enum):
    Bangumi = "番剧"
    """番剧"""
    Movie = "电影"
    """电影"""
    Guochuang = "国创"
    """国创"""
    Documentary = "纪录片"
    """纪录片"""
    Normal = "用户投稿视频"
    """用户投稿视频"""


def get_video_type(video_type: int) -> VideoType:
    """
    通过视频信息判断视频的是什么类型
    """
    match video_type:
        case 1:
            return VideoType.Bangumi
        case 2:
            return VideoType.Movie
        case 3:
            return VideoType.Guochuang
        case 4:
            return VideoType.Guochuang
        case _:
            return VideoType.Normal


def get_version() -> str:
    """从pyproject.toml中获取版本"""
    raise NotImplementedError


def show_version(enabled: bool):
    """显示版本信息"""
    if enabled:
        version = get_version()
        print(f"Bili23 Version: {version}")


def get_video_info(url: str) -> Dict[str, Any]:
    """
    获取视频信息
    """
    # TODO: 这里发送请求过去，大概就是写一个 request.get()  什么的方法过去就是了

    raise NotImplementedError


def generate_qr_code(data: str):
    """生成二维码的图片"""
    qrcode = QRCode()
    qrcode.add_data(data)
    qrcode.print_ascii()


def listen_login_status(api: Api, login_qr_code_info: LoginQRCodeInfo, seconds: int = 1):
    """监听登录状态

    每隔一定是时间发送一次请求判断是否登录成功
    """
    while True:
        code = api.check_login_state(login_qr_code_info.key)
        time.sleep(seconds)
        match code:
            case 0:
                user_info = api.get_user_info()
                api.config.user_info = user_info
                save_config(api.config)
                print(":star: 登录成功")
                break
            case 86090:
                print("请在设备侧确认登录")
            case 86038:
                login_qr_code_info = api.get_login_qr_code_info()
                generate_qr_code(login_qr_code_info.url)
            case _:
                continue


# command 它们就应该留在这个目录或者 cli.py
########################################
@app.command()
def login():
    """
    登录
    """

    # TODO: 后续将和用户有关的命令集成到 user 这个子命令中如  bili23 user login
    api = Api()
    login_qr_code_info = api.get_login_qr_code_info()
    generate_qr_code(login_qr_code_info.url)

    listen_login_status(api, login_qr_code_info)


@app.command()
def repo():
    """
    本地仓库列表

    用来查看已经下载的视频，所在的位置，查看视频的详情信息等，
    """
    raise NotImplementedError


@app.command()
def config():
    """查看 or 编辑 配置"""
    raise NotImplementedError


# TODO： 需要支持输入多个url 进行下载
@app.callback()
def main(
    version: Annotated[
        bool,
        Option("--version", "-v", callback=show_version, help="show version", is_eager=True),
    ] = False,
):
    """
    BiliBili 视频下载工具
    """
    check_config()
