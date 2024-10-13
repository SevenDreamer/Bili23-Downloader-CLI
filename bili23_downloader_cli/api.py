from typing import Any, Dict, Optional, Tuple
from pydantic import BaseModel
from requests import Session
from requests.auth import HTTPProxyAuth, AuthBase
from rich import print

from bili23_downloader_cli.config import UserInfo, load_config

BASE_URL = "https://api.bilibili.com"
BASE_LOGIN_URL = "https://passport.bilibili.com/x/passport-login/web/qrcode"


# schema
class LoginQRCodeInfo(BaseModel):
    url: str
    key: str


class Api:
    def __init__(self):
        self.config = load_config()
        self.init_session()

    def get_login_qr_code_info(self) -> LoginQRCodeInfo:
        """
        获取登录二维码的信息
        """
        url = f"{BASE_LOGIN_URL}/generate"
        print(url)
        data = self.get(url)
        return LoginQRCodeInfo(url=data["url"], key=data["qrcode_key"])

    def check_login_state(self, key: str) -> int:
        """
        获取用户登录状态

        :param key: LoginQRCodeInfo.key

        :return code: 登录状态
        """
        url = f"{BASE_LOGIN_URL}/poll?qrcode_key={key}"
        data = self.get(url)

        return data["code"]

    def get_user_info(self, refreh: bool = False) -> UserInfo:
        """获取用户信息"""
        url = f"{BASE_URL}/x/web-interface/nav"
        print("user_info", self.session.cookies.items())

        # 将扫码后得到的cookie放到headers.cookie里面
        self.session.headers["Cookie"] = ";".join([f"{key}={value}" for (key, value) in self.session.cookies.items()])
        data = self.get(url)

        # if refreh:
        #     self.session.headers["Cookie"] += f"SESSDATA={user_sessdata}"  # type: ignore

        # headers = {"Cookie": f"SESSDATA={self.session.cookies.get_dict()['SESSDATA']}"}
        # data = self.get(url, headers)

        print(data)
        return UserInfo(
            uname=data["uname"],
            face=data["face"],
            sessdata=self.session.cookies.get_dict()["SESSDATA"],
        )

    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
        auth: Optional[AuthBase] = None,
    ) -> Dict[str, Any]:
        """GET 请求"""
        res = self.session.get(url, headers=headers, proxies=proxies, auth=auth)
        result = res.json()

        # 判断状态码 TODO: 可能需要完善
        if res.status_code != 200:
            print(res.json())

        # 判断消息内容
        if result["code"] != 0:
            print(result["message"])

        return result["data"]

    def init_session(self):
        """初始化session"""
        self.session = Session()
        self.session.headers = self.headers  # type: ignore
        self.session.auth = self.auth
        self.session.proxies = self.proxies

    @property
    def proxies(self) -> Dict[str, str]:
        proxy = self.config.proxy
        if proxy and proxy.enabled:
            return {
                scheme: f"{proxy.ip}{':'if proxy.port else ''}{proxy.port if proxy.port else''}"
                for scheme in ["http", "https"]
            }
        else:
            return {}

    @property
    def auth(self) -> Optional[HTTPProxyAuth]:
        """
        设置请求验证

        如果代理开启，并且启用了用户验证
        """
        proxy = self.config.proxy
        if proxy:
            if proxy.enabled and proxy.auth_enabled:
                return HTTPProxyAuth(proxy.username, proxy.password)
            else:
                return None

    @property
    def headers(self):
        headers: Dict[str, str] = {}
        headers["Cookie"] = "CURRENT_FNVAL=4048;"
        headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
        )
        return headers

    def set_headers(
        self,
        referer_url: Optional[str] = None,
        cookie: Optional[str] = None,
        chunk: Optional[Tuple[int, int]] = None,
        download: bool = False,
    ):
        """设置请求头"""
        # headers: Dict[str, str] = {}
        # headers["Cookie"] = "CURRENT_FNVAL=4048;"
        # headers["User-Agent"] = (
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
        # )

        if referer_url:
            self.session.headers["Referer"] = referer_url

        if chunk:
            start, end = chunk
            self.session.headers["Range"] = f"bytes={start}-{end}"

        if cookie:
            self.session.headers["Cookie"] += f"SESSDATA={cookie};"  # type: ignore

        if download:
            self.session.headers["Accept"] = "*/*"
            self.session.headers["Accept-Encoding"] = "identity"
            self.session.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
            self.session.headers["Origin"] = "https://www.bilibili.com"
            self.session.headers["Priority"] = "u=1, i"
