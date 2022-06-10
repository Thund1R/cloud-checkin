from config import checkin
import requests
import json
import hashlib

everphoto = checkin.get("everphoto")


def get_pwd_md5(eppwd):
    salt = "tc.everphoto."
    pwd = salt + eppwd
    md5 = hashlib.md5(pwd.encode())
    return md5.hexdigest()


def checkin(everphoto):
    phone = everphoto.get("phone")
    pwd = everphoto.get("password")
    header = {
        "user-agent": "EverPhoto/4.5.0 (Android;4050002;MuMu;23;dev)",
        "application": "tc.everphoto",
    }
    result = "无法获取"
    name = "无法获取"
    todayReward = "无法获取"
    tomorrowReward = "无法获取"
    totalReward = "无法获取"
    if phone and pwd:
        try:
            login_url = "https://web.everphoto.cn/api/auth"
            password = get_pwd_md5(pwd)
            mobile = phone if phone[0] == "+" else "+86" + phone
            data = {
                "mobile": mobile,
                "password": password
            }
            login_res = requests.post(
                login_url, data=data, headers=header).json()
            check_url = "https://openapi.everphoto.cn/sf/3/v4/PostCheckIn"
            if login_res['code'] == 0:
                name = login_res["data"]["user_profile"]["name"]
                header["authorization"] = "Bearer " + \
                    login_res["data"]["token"]
                head = {
                    "content-type": "application/json",
                    "host": "openapi.everphoto.cn",
                    "connection": "Keep-Alive",
                }
                header.update(head)
                checkin_res = requests.post(check_url, headers=header).json()
                if checkin_res['code'] == 0:
                    tomorrowReward = str(
                        checkin_res["data"]["tomorrow_reward"]/1024/1024) + "M"
                    totalReward = str(
                        round(checkin_res["data"]["total_reward"]/1024/1024/1024, 2))+"G"
                    if checkin_res["data"]["checkin_result"] == True:
                        result = "签到成功"
                        todayReward = str(
                            checkin_res["data"]["reward"]/1024/1024) + "M"
                    else:
                        result = "签到重复"
                else:
                    result = "签到失败"
            else:
                result = "登陆失败" + login_res['message']
        except Exception as errorMsg:
            result = "签到异常" + repr(errorMsg)
        print("EVERPHOTO", result)
        return {
            "账号": name,
            "签到结果": result,
            "今天奖励": todayReward,
            "明天奖励": tomorrowReward,
            "总共奖励": totalReward
        }
    else:
        print("EVERPHOTO配置缺失")
        return None


def main():
    print("EVERPHOTO签到开始")
    detail = list(filter(None, list(map(checkin, everphoto))))
    if len(detail):
        res = {"project": "EVERPHOTO", "detail": detail}
    else:
        res = None
    return res


if __name__ == '__main__':
    main()
