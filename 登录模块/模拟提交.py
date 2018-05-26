from 登录模块.获取cookies import GetCookie
import 登录模块.参数 as config
from urllib.parse import urlencode
import requests
import json
# postChoiceCheckbox
listFormData = [
    # Inside view
    [0] * 8,                    # Conversation 1-1
    [0] * 8,                    # Conversation 1-2
    [0] * 8,                    # Conversation 2-1
    [0] * 8,                    # Conversation 2-2
    [0] * 8,                    # Real life practice

    # Outside view
    [1, 1, 1, 1, 1, 1, 1, 1],   # Outside view 1
    [1, 0, 1, 1, 1, 1, 1, 1],   # Outside view 2
    [1, 1, 0, 1, 0, 1, 1, 1],   # Outside view 3
    [1, 0, 0, 1, 0, 1, 0, 0],   # Outside view 4
    [0] * 8,                    # Outside view 5

    # Listening in
    [1] * 8,                    # Talk 1
    [1] * 8,                    # Talk 2
    [1, 1, 0, 0, 1, 1, 0, 1],   # Passage 1-1
    [1, 1, 0, 1, 0, 1, 1, 1],   # Passage 1-3
    [0, 0, 0, 0, 0, 1, 1, 0],   # Passage 1-1
    [1] * 8,                    # Passage 2-1
    [0, 1, 1, 1, 1, 1, 0, 1],   # Passage 2-2
    # Presentation skills
    [0] * 8,                    # Learning
    [0] * 8,                    # Practice

    # Pronunciation
    [0] * 8,                    # Pronunciation 1
    [0] * 8,                    # Pronunciation 2
    [0] * 8,                    # Pronunciation 3
    [0] * 8,                    # Pronunciation 4
    [0] * 8,                    # Pronunciation 5

    # Unit test
    [1] * 8,                    # Unit test
]

def post_one_web(UnitID, SectionID, SisterID, cookies):


    print(f'Unit = {UnitID}, SectionID = {SectionID}, SisterID = {SisterID}')

    RequestURL = "http://" + config.host + ':' + str(config.port) + \
                 '/book/' + config.bookNum + '/initPage.php'

    FormData = {
        'UnitID': UnitID,
        'SectionID': SectionID,
        'SisterID': SisterID
    }
    header = {
        'Host': config.host + ':' + str(config.port),
        'Connection': 'keep-alive',
        'Content-Length': str(len(urlencode(FormData))),
        'Cache-Control': 'no-cache',
        'Origin': 'http://' + config.host + ':' + str(config.port),
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': RequestURL,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no - cache',
        'X-Requested-With': 'XMLHttpRequest',
    }
    #cookies['NCCE'] = '822290a86589bc160feabc4dceb4bbe2'
    ansResponse = requests.post(url=RequestURL, headers =header, data = FormData, cookies = cookies)
    ansResponse.encoding = 'utf-8'
    #print(ansResponse.text)
    answer = json.loads(ansResponse.text)


    cheakAns = str(answer['key']).replace('^', '')
    if cheakAns.isdigit() or cheakAns.isupper():
        postChoiceRadio(answer, cookies)
    else:
        postFillText(answer, cookies)
    #print(answer)
    return

def postFillText(ansjson: dict, cookies: dict) -> None:
    ansFilter = []
    for ans in ansjson['key'].split('^'):
        if ans.find('|')!= -1:
            ansFilter.append(ans[:ans.find('|')])
        else:
            ansFilter.append(ans)
    ansFormData = {
        'ItemID': ansjson['ItemID'],
        'answer': (ansFilter),
    }
    print('填空题', ansFormData)
    header = {
        'Host': config.host + ':' + str(config.port),
        'Connection': 'keep-alive',
        'Content-Length': str(len(myurlencode(ansFormData))),
        'Cache-Control': 'no-cache',
        'Origin': 'http://' + config.host + ':' + str(config.port),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
    }

    postFillTextURL = 'http://' + config.host + ':' + str(config.port) +'/book/' + config.bookNum + '/postFillText.php'
    postResult = requests.post(url = postFillTextURL, headers = header, cookies = cookies, data = myurlencode(ansFormData))
    print(postResult.text)

def postChoiceRadio(ansjson: dict, cookies: dict) -> None:
    ansFormData = {
        'ItemID': ansjson['ItemID'],
        'answer': ansjson['key'].split('^'),
    }
    print('选择题', ansFormData)
    header = {
        'Host': config.host + ':' + str(config.port),
        'Connection': 'keep-alive',
        'Content-Length': str(len(myurlencode(ansFormData))),
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
    }
    postChoiceRadioURL = 'http://' + config.host + ':' + str(config.port) +'/book/' + config.bookNum + '/postChoiceRadio.php'
    postResult = requests.post(url = postChoiceRadioURL, headers = header, cookies = cookies, data = myurlencode(ansFormData))
    print(postResult.text)

def myurlencode(dictExp:dict) -> str:
    print(dictExp)
    reStr = 'ItemID=' + dictExp['ItemID']
    for ans in dictExp['answer']:
        reStr += u'&answer%5B%5D=' + ans
    return reStr

if __name__ == '__main__':
    Cookie = GetCookie()
    for row, line in enumerate(listFormData):
        for col, data in enumerate(line):
            # print(row, col, data)
            UnitID = col + 1
            if row <= 4: # Inside view
                SectionID = 1
                SisterID = row + 1
            elif row <= 9:  # Outside view
                SectionID = 2
                SisterID = row - 4
            elif row <= 16: # Listening in
                SectionID = 3
                SisterID = row - 9
            elif row < 18: # Presentation skills
                SectionID = 4
                SisterID = row - 16
            elif row < 23: # Pronunciation
                SectionID = 5
                SisterID = row - 18
            else: # Unit test
                SectionID = 6
                SisterID = row - 23
            if data is not 0:
                post_one_web(UnitID, SectionID, SisterID, Cookie)
