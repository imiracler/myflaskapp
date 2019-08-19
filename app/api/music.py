from flask import Blueprint, current_app, jsonify, request
from flask_login import login_required, logout_user, current_user
from sts.sts import Sts
import random

music = Blueprint("music", __name__, template_folder='templates', static_folder='static', static_url_path="/static")

@music.route("/music", methods=["GET"])
@login_required
def get_book():
    return "this is my first book"


@music.route('/', defaults={'path': ''})
@music.route('/<path:path>')
def index(path):
  return render_template('index.html')


@music.route("/music/secret", methods=["GET"])
def get_secretinfo():
    result = dict()
    result["SecretId"] = current_app.config['SECRETID']
    result["SecretKey"] = current_app.config['SECRETVALUE']
    return jsonify(result)

@music.route("/music/getcredential", methods=["GET"])
def get_credential():
    config = {
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        # 固定密钥
        'secret_id': current_app.config['SECRETID'],
        # 固定密钥
        'secret_key': current_app.config['SECRETVALUE'],
        # 是否需要设置代理
        'proxy': {
            'http': '',
            'https': ''
        },
        # 换成你的 bucket
        'bucket': 'banbantian-1256944551',
        # 换成 bucket 所在地区
        'region': 'ap-shanghai',
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的目录，例子：* 或者 a/* 或者 a.jpg
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            'name/cos:PutObject',
            'name/cos:PostObject',
            # 分片上传
            'name/cos:InitiateMultipartUpload',
            'name/cos:ListMultipartUploads',
            'name/cos:ListParts',
            'name/cos:UploadPart',
            'name/cos:CompleteMultipartUpload',
            'name/cos:GetObject'
        ]

    }

    sts = Sts(config)
    response = sts.get_credential()
    print(type(response))
    return jsonify(response)


@music.route("/music/lottery", methods=["POST"])
def get_lottery_result():
    import pdb
    res = request.json
    data = res["ids"]
    period = res["periods"]
    def strategy(data: list):
        # 两个选一个
        ten_num = [i for i in range(10)]
        res = []
        a = random.choice(data)
        res.append(a)
        if data[0] != data[1]:
            ten_num.remove(data[0])
            ten_num.remove(data[1])
        else:
            ten_num.remove(a)
        c = random.sample(ten_num, 2)
        res.append(c[0])
        res.append(c[1])
        return res

    def strategy_2():
        # 随机
        return random.sample([i for i in range(10)], 3)

    def strategy_3(data: list):
        # 两个都要

        num = [i for i in range(10)]
        res = []
        if data[0] != data[1]:
            res.append(data[0])
            res.append(data[1])
            num.remove(data[0])
            num.remove(data[1])
            c = random.sample(num, 1)
            res.append(c[0])
        else:
            res.append(data[0])
            num.remove(data[0])
            c = random.sample(num, 2)
            res.append(c[0])
            res.append(c[1])
        return res

    if period % 3 == 0:
        killedNumber = strategy_3([5, 8] if period == 0 else data)
    elif period % 3 == 1:
        killedNumber = strategy_2()
    else:
        killedNumber = strategy([2, 4] if period == 0 else data)

    return jsonify({"data":killedNumber})
