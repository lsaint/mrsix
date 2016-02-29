
import time, hashlib

import requests


class WechatBasic(object):

    def __init__(self, appid, appsecret):
        self.__appid = appid
        self.__appsecret = appsecret

        self.__access_token = None
        self.__access_token_expires_at = None
        self.__jsapi_ticket = None
        self.__jsapi_ticket_expires_at = None


    def _check_official_error(self, json_data):
        """
        检测微信公众平台返回值中是否包含错误的返回码
        :raises OfficialAPIError: 如果返回码提示有错误，抛出异常；否则返回 True
        """
        if "errcode" in json_data and json_data["errcode"] != 0:
            raise OfficialAPIError("{}: {}".format(json_data["errcode"], json_data["errmsg"]))


    def _get(self, url, **kwargs):
        """
        使用 GET 方法向微信服务器发出请求
        :param url: 请求地址
        :param kwargs: 附加数据
        :return: 微信服务器响应的 json 数据
        :raise HTTPError: 微信api http 请求失败
        """
        return self._request(
            method="get",
            url=url,
            **kwargs
        )


    def _request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {
                "access_token": self.access_token,
            }
        if isinstance(kwargs.get("data", ""), dict):
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        response_json = r.json()
        self._check_official_error(response_json)
        return response_json


    def grant_token(self):
        """
        获取 Access Token
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        response_json = self._get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.__appid,
                "secret": self.__appsecret,
            })
        self.__access_token = response_json['access_token']
        print("grant_token", self.__access_token)
        self.__access_token_expires_at = int(time.time()) + response_json['expires_in']
        return response_json


    @property
    def access_token(self):
        if self.__access_token:
            now = time.time()
            if self.__access_token_expires_at - now > 60:
                return self.__access_token
        self.grant_token()
        return self.__access_token


    def grant_jsapi_ticket(self):
        """
        获取 Jsapi Ticket
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        # force to grant new access_token to avoid invalid credential issue
        self.grant_token()

        response_json = self._get(
            url="https://api.weixin.qq.com/cgi-bin/ticket/getticket",
            params={
                "access_token": self.access_token,
                "type": "jsapi",
            }
        )
        self.__jsapi_ticket = response_json['ticket']
        print("grant_jsapi_ticket", self.__jsapi_ticket)
        self.__jsapi_ticket_expires_at = int(time.time()) + response_json['expires_in']
        return response_json


    @property
    def jsapi_ticket(self):
        if self.__jsapi_ticket:
            now = time.time()
            if self.__jsapi_ticket_expires_at - now > 60:
                return self.__jsapi_ticket
        self.grant_jsapi_ticket()
        return self.__jsapi_ticket


    def generate_jsapi_signature(self, timestamp, noncestr, url, jsapi_ticket=None):
        """
        使用 jsapi_ticket 对 url 进行签名
        :param timestamp: 时间戳
        :param noncestr: 随机数
        :param url: 要签名的 url，不包含 # 及其后面部分
        :param jsapi_ticket: (可选参数) jsapi_ticket 值 (如不提供将自动通过 appid 和 appsecret 获取)
        :return: 返回sha1签名的hexdigest值
        """
        if not jsapi_ticket:
            jsapi_ticket = self.jsapi_ticket
        data = {
            'jsapi_ticket': jsapi_ticket,
            'noncestr': noncestr,
            'timestamp': timestamp,
            'url': url,
        }
        keys = list(data.keys())
        keys.sort()
        data_str = '&'.join(['%s=%s' % (key, data[key]) for key in keys])
        signature = hashlib.sha1(data_str.encode('utf-8')).hexdigest()
        return signature


class OfficialAPIError(Exception):
    """
    微信官方API请求出错异常
    """
    pass

