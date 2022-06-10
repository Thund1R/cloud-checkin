from config import checkin
import time
import requests
import json

glados = checkin.get("glados")


def checkin(glados):
    result = "无法获取"
    email = "无法获取"
    leftDays = "无法获取"
    message = "无法获取"
    cookie = glados.get("cookie")
    if cookie:
        checkin_url = "https://glados.rocks/api/user/checkin"
        status_url = "https://glados.rocks/api/user/status"
        payload = {
            'token': 'glados.network'
        }
        headers = {'cookie': cookie,
                   'referer': "https://glados.rocks/console/checkin",
                   'origin': "https://glados.rocks",
                   'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
                   'content-type': 'application/json;charset=UTF-8'}
        try:
            checkin_res = requests.post(
                checkin_url, headers=headers, data=json.dumps(payload)).json()
            status = requests.get(status_url, headers=headers).json()
            message = checkin_res['message']
            if 'list' in checkin_res:
                result = "签到成功"
                email = status['data']['email']
                leftDays = status['data']['leftDays'].split('.')[0]
            else:
                result = "签到失败"
        except Exception as errorMsg:
            result = "签到异常"
            message = repr(errorMsg)
        print("GLADOS", result+message)
        return {
            "账号": email,
            "签到结果": result,
            "剩余天数": leftDays,
            "签到信息": message
        }
    else:
        return None


def main():
    print("GLADOS签到开始")
    detail = list(filter(None, list(map(checkin, glados))))
    if len(detail):
        res = {"project": "GLADOS", "detail": detail}
    else:
        res = None
    return res


if __name__ == '__main__':
    main()
