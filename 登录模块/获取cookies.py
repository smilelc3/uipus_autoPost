import requests
import 登录模块.参数 as config
from urllib.parse import urlencode
from bs4 import BeautifulSoup


RequestURL = "http://" + config.host + ':' + str(config.port) + '/index.php'

FormData = {
    'username': config.username,
    'password': config.password,
    'Input2': '登+录',
}
header1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': config.host + ':' + str(config.port),
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0)',
    'Upgrade-Insecure-Requests': '1',

}
header2 = {
    'Host': config.host + ':' + str(config.port),
    'Connection': 'keep-alive',
    'Content-Length': str(len(urlencode(FormData))),
    'Cache-Control': 'no-cache',
    'Origin': 'http://' + config.host + ':' + str(config.port),
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Referer': RequestURL,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

header3 = {
    'Host': config.host + ':' + str(config.port),
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Pragma': 'no-cache',
    'X-Prototype-Version': '1.7.2',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

}

def GetCookie():
    s=requests.session()
    #print(s.cookies.get_dict())#先打印一下，此时一般应该是空的。
    #需要先get创建一个cookie
    Get = s.get(RequestURL, headers = header1)
    print('GET_cookies = ', 'NCCE=' + s.cookies.get_dict()['NCCE'])
    #time.sleep(0.5)

    #print(Get.headers)
    res=s.post(RequestURL,headers = header2, data = FormData, cookies = s.cookies.get_dict())
    res.encoding = 'utf-8'
    #print(res.text)

    studentLoginURL = "http://" + config.host + ':' + str(config.port) + '/login/hpindex_student.php'
    studentLoginCookies = s.cookies.get_dict()
    studentLoginCookies['NHCELoginCounter']: '0'
    response = s.get(url = studentLoginURL,
                     cookies = studentLoginCookies,
                     headers = header1)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')


    myClass = soup.select_one('#BookClassDIV > table.myclass_table > tr > td > ul > li > a')
    #print(myClass.get('href'))
    LoginClassURL = "http://" + config.host + ':' + str(config.port) + myClass.get('href')
    LoginClassRe = s.get(url = LoginClassURL, headers = header1, cookies = s.cookies.get_dict())
    LoginClassRe.encoding = 'utf-8'
    #print(LoginClassURL)

    refresh = BeautifulSoup(LoginClassRe.text, 'lxml')
    URL = refresh.find_all('meta', attrs={'http-equiv':'refresh'})[0].get('content')
    refreshURL = URL[URL.find("URL=") + len('URL='):]
    ActionURL = "http://" + config.host + ':' + str(config.port) + refreshURL
    Action = s.get(url = ActionURL, headers = header1, cookies = s.cookies.get_dict())




    LoginURL = "http://" + config.host + ':' + str(config.port) + '/template/loggingajax.php'
    LoginData = {
        'whichURL': '/book/' + config.bookNum + 'index.php'
    }

    Login = s.get(url = LoginURL, headers = header3, cookies = s.cookies.get_dict(),data = LoginData)

    #print(Login.text)
    return s.cookies.get_dict()

if __name__ == '__main__':
    GetCookie()
