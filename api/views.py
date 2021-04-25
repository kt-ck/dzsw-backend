from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64

def getScore(TEXT):
    #接口地址
    url ="http://ltpapi.xfyun.cn/v2/sa"
    #开放平台应用ID
    x_appid = "171d0bb9"
    #开放平台应用接口秘钥
    api_key = "32ade747c56bc80f39bf6a00cc7ca46b"
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()

    return result.decode('utf-8')

def _getKeyWord(TEXT):
    url ="https://ltpapi.xfyun.cn/v1/ke"
    #开放平台应用ID
    x_appid = "171d0bb9"
    #开放平台应用接口秘钥
    api_key = "32ade747c56bc80f39bf6a00cc7ca46b"

    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    return result

@csrf_exempt
def getTextEmotionScore(request):
    if request.method == 'POST':
        text = request.body
        text =  str(text, encoding = "utf-8")
        text_json = json.loads(text)
        text = text_json['diary']
        result_str = getScore(text)
        result_json = json.loads(result_str)
        success = result_json['desc']
        # print(success)
        if success == "success":
            score = result_json['data']['score']
            sentiment = result_json['data']['sentiment']
        else:
            score = '0.5'
            sentiment = '0'
        return_data = {'score': score, 'sentiment': sentiment}
        return JsonResponse(return_data)

@csrf_exempt
def getKeyWord(request):
    if request.method == 'POST':
        text = request.body
        text =  str(text, encoding = "utf-8")
        text_json = json.loads(text)
        text = text_json['diary']
        result_str = _getKeyWord(text)
        result_json = json.loads(result_str)
        success = result_json['desc']
        if success == "success":
            mainKey = result_json['data']['ke']
        else:
            mainKey = "检测不出任何关键词"
        return_data = {'key': mainKey}
        res = JsonResponse(return_data)
    return res


def test(request):
    # response = JsonResponse({})
    return HttpResponse("Hello world!")
