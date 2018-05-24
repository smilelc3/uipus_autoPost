import requests
import 登录模块.参数 as config
from urllib.parse import urlencode

RequestURL = "http://" + config.host + ':' + str(config.port) + '/index.php'

FormData = {
    'username': config.username,
    'password': config.password,
    'Input2': '登 录',
}

header = {
    'Host': config.host + ':' + str(config.port),
    'Connection': 'keep-alive',
    'Content-Length': str(len(urlencode(FormData))),
    'Cache-Control': 'max-age=0',
    'Origin': 'http://' + config.host + ':' + str(config.port),
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Referer': RequestURL,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}


def GetCookie():
    s=requests.session()
    # print(s.cookies.get_dict())#先打印一下，此时一般应该是空的。
    res=s.post(RequestURL,headers = header, data = FormData)
    #print(RequestURL, res.content)
    print(s.cookies.get_dict())
    return s.cookies.get_dict()

if __name__ == '__main__':
    GetCookie()
