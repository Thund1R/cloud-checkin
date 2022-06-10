import os
from config import checkin
import push
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for file in os.listdir(os.path.join(os.path.dirname(__file__), 'checkin')):
    if not file.startswith('_') and file.endswith('py'):
        exec('from checkin import {}'.format(file.replace('.py', '')))


def run_checkin(key):
    if checkin.get(key):
        return eval(key).main()
    else:
        return None


def main():
    res = list(map(run_checkin, list(checkin.keys())))
    res = list(filter(None, res))
    push.push_msg(res)


def main_handler(event, context):
    main()


def handler(event, context):
    main()


if __name__ == '__main__':
    main()
