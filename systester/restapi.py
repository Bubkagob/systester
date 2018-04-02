# coding=utf-8
# (Кодировка)
# http://docs.python-requests.org/en/master/user/quickstart/
import time
import requests


def read_tag(tag_name):
    return requests.get("http://127.0.0.1:8081/read.json?tag="+tag_name)


def HttpGet(command):
    try:
        # res = requests.get('http://127.0.0.1:8081' + command, timeout=2.0)
        # res = requests.request("get", "http://127.0.0.1:8081" + command, timeout=2.0)
        with requests.Session() as s:
            s.keep_alive = True
            res = s.get("http://127.0.0.1:8081" + command)
            s.close()

        if res.status_code == 200:
            return res.json()
        elif res.status_code == 204:
            return {}
        else:
            raise Exception("{}: {}: {}".format(
                command, res.status_code, res.text))
    except Exception as e:
                # if connection error occurs, we are here
        raise Exception("{}: {}".format(command, str(e)))

# return tuple (v, q, t)


def ReadTag(tag_name_or_id):
    res = HttpGet('/read.json?tag=' + tag_name_or_id)

    if "v" in res:
        return (res["v"], res["q"], res["t"])
    else:
        raise Exception("Result is empty for {}".format(tag_name_or_id))


def WriteTag(tag_name_or_id, value):
    if isinstance(value, bool):
        value = "1" if value else "0"
    HttpGet("/write.json?tag={}&val={}".format(tag_name_or_id, value))


def TestTag(tag_name_or_id, value, quality=None, silent=True):
    vqt = ReadTag(tag_name_or_id)

    if value is not None:
        remote_value = vqt[0]
        # for floats we need reasonable accuracy
        if isinstance(value, float):
            value = int(value * 100) / 100
            remote_value = int(remote_value * 100) / 100

        if value != remote_value:
            if isinstance(value, int):
                raise Exception('{}: expected value {}<0x{:02X}>; got {}<0x{:02X}>'.format(
                    tag_name_or_id, value, value, remote_value, remote_value))
            else:
                raise Exception('{}: expected value {}; got {}'.format(
                    tag_name_or_id, value, remote_value))

    if quality is not None:
        if quality != vqt[1]:
            raise Exception('{}: expected quality 0x{:02X}; got 0x{:02X}'.format(
                tag_name_or_id, quality, vqt[1]))

    if not silent:
        if quality is None or quality == 0:
            print("OK: {}={}".format(tag_name_or_id, value))
        elif value is None:
            print("OK: {}=NA[{:02X}]".format(tag_name_or_id, quality))
        else:
            print("OK: {}={}[{:02X}]".format(tag_name_or_id, value, quality))


def WaitTag(tag_name_or_id, waited_value, timeout_sec, silent=False):
    if not silent:
        print("Wait")
        # print("Wait {}={} ({} sec)...".format(tag_name_or_id,
        # waited_value, timeout_sec), end="", flush=True)
    t1 = time.perf_counter()
    while (time.perf_counter() - t1) < timeout_sec:
        vqt = ReadTag(tag_name_or_id)
        if waited_value == vqt[0] and vqt[1] == 0:
            if not silent:
                print("OK")
            return
        time.sleep(0.1)
    raise Exception("Timeout waiting {}={}".format(
        tag_name_or_id, waited_value))


def SafeStopCore():
    try:
        HttpGet('/stop')
    except NameError as ne:
        print(ne)
