from flask import Blueprint, current_app, jsonify, request
from flask_login import login_required, logout_user, current_user
from sts.sts import Sts

music = Blueprint("music", __name__)

@music.route("/music", methods=["GET"])
@login_required
def get_book():
    return "this is my first book"


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
