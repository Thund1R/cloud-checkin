from config import push
import json
import requests


def listtomd(content):
    con = ""
    for i in range(0, len(content)):
        con = con + '【'+content[i]['project']+'】\n\n'
        for j in range(0, len(content[i]['detail'])):
            for key, value in content[i]['detail'][j].items():
                con = con+key+":"+str(value)+'\n\n'
    con = con+'---\n\n'
    return con


def push_msg(content):
    pushplus = push.get("pushplus")
    server = push.get("server")
    title = "CloudCheckin云签到"
    content = listtomd(content)
    if pushplus:
        push_url = 'http://www.pushplus.plus/send'
        data = {
            "token": pushplus,
            "template": "markdown",
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        res = requests.post(push_url, data=body, headers=headers)
        print("Pushplus:", res.text)
    if server:
        push_url = "https://sctapi.ftqq.com/{}.send".format(server)
        data = {
            "title": title,
            "desp": content
        }
        res = requests.post(push_url, data)
        print("Server酱:", res.text)
