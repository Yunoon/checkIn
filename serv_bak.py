import base64
import datetime
import time

import qrcode
import requests
from flask import Flask, render_template, request, make_response
import config

import base64
from Crypto.Cipher import AES

import os
import json
import logging

from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config.from_object(config)

app.wsgi_app = ProxyFix(app.wsgi_app)

basedir = os.path.abspath(os.path.dirname(__file__))
secret = "114514" #密钥当然改了的啦～

import socket

# 获取计算机名称
hostname = socket.gethostname()
# 获取本机IP
ip = socket.gethostbyname(hostname)


def aes_decode(data, key):
    """

    :param data:
    :type data:
    :param key:
    :type key:
    :return:
    :rtype:
    """

    try:
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    except Exception as e:
        decrypted_text = 0
    return decrypted_text


# 加密
def aes_encode(data, key):
    """

    :param data:
    :type data:
    :param key:
    :type key:
    :return:
    :rtype:
    """
    while len(data) % 16 != 0:  # 补足字符串长度为16的倍数
        data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
    data = str.encode(data)
    aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
    return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # 加密


@app.route('/')
def index():
    """

    :return:
    :rtype:
    """
    test = 1
    return render_template('index.html', test='This is index page')


@app.route('/getPic', methods=['GET'])
def show_photo():
    now = int(round(time.time() * 1000))
    check = "http://172.24.93.172:8080/writename?code=" + aes_encode(data=str(now), key=secret)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(check)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('qr.png')
    image_data = open("qr.png", "rb").read()

    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route("/writename", methods=["GET"])
def writename_get():  # noqa: E501
    """姓名接口

     # noqa: E501

    :param name:
    :type name: str

    :rtype: str
    """
    name = request.args.get("name")
    code = request.args.get("code")

    return render_template("checkIn.html", code=code)


@app.route("/checkIn", methods=["POST"])
def checkin():  # noqa: E501
    """姓名接口

     # noqa: E501

    :param name:
    :type name: str

    :rtype: str
    """
    name = request.form['name']
    code = request.form['code']
    status = request.form['status']
    ua = request.headers['user-agent']
    ip = request.remote_addr

    file = r'./check.txt'
    time_check = aes_decode(data=code, key=secret)
    time_local = time.localtime(int(time_check) / 1000)
    time_check = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    data = "姓名: " + name + " status: " + status + " time: " + time_check + " ua: " + ua + " ip: " + ip
    print(data)
    try:
        data = name + ": " + time_check + '\n'
    except:
        return "<script>alert(\"签到失败，在想什么呢？\");window.location.href=\"http://172.24.93.172:8080\";</script>"

    with open(file, 'a+') as f:
        f.write(data)
    return "<script>alert(\"签到成功, 快去学习吧～\");window.location.href=\"http://cqustoj.yuno0n.top/\";</script>"


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False

    app.run(host="0.0.0.0", port=8080)
