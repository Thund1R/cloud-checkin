from config import checkin
import requests
import json

sspanel = checkin.get("sspanel")


def checkin(sspanel):
    email = sspanel.get("email")
    password = sspanel.get("password")
    url = sspanel.get("url")
    emailmsg = email if email else "无法获取"
    urlmsg = url if url else "无法获取"
    msg = "无法获取"
    if email and password and url:
        try:
            session = requests.session()
            session.get(url=url, verify=False)
            login_url = url + "/auth/login"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            post_data = "email=" + \
                email.replace("@", "%40") + "&passwd=" + password + "&code="
            post_data = post_data.encode()
            session.post(login_url, post_data, headers=headers, verify=False)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Referer": url + "/user",
            }
            response = session.post(url + "/user/checkin",
                                    headers=headers, verify=False)
            msg = response.json().get("msg")
        except Exception as errorMsg:
            msg = repr(errorMsg)
        print("SSPANEL", msg)
        return {
            "账号": emailmsg,
            "网址": urlmsg,
            "签到信息": msg
        }
    else:
        print("SSPANEL配置缺失")
        return None


def main():
    print("SSPANEL签到开始")
    detail = list(filter(None, list(map(checkin, sspanel))))
    if len(detail):
        res = {"project": "SSPANEL", "detail": detail}
    else:
        res = None
    return res


if __name__ == "__main__":
    main()
