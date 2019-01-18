from django.shortcuts import render, redirect
from rest_framework import viewsets
from users.serializers import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from config_default import configs
from qiniu import Auth
import time
import random
import string
from rest_framework.authtoken.models import Token

import pdb

from django.contrib.auth.hashers import make_password, check_password


# 注册
class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        if User.objects.filter(username__exact=data.get('username')):
            return Response({"stateCode": 201, "msg": "用户已存在"}, 201)
        if User.objects.filter(email__exact=data.get('email')):
            return Response({"stateCode": 202, "msg": "邮箱已被注册"}, 201)
        new_user = {
            'username': data.get('username'),
            'email': data.get('email'),
            'password': make_password(data.get('password')),
            'user_image_url': data.get('user_image_url')
        }
        # print(new_user)
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"stateCode": 200, "msg": "注册成功"}, 200)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# 登录
class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            user = None
        if user:
            if check_password(password, user.password):
                serializer = UserSerializer(user)
                new_data = serializer.data
                # 记忆已登录用户，作为用户是否拥有某项权限的认证
                # self.request.session['user_username'] = user.username
                token = Token.objects.get(user_id=user.id)
                new_obj = {
                    'username': new_data.get('username'),
                    'token': token.key,
                    'user_image_url': new_data.get('user_image_url')
                }
                # print(token)
                return Response({"stateCode": 200, "msg": new_obj}, status=HTTP_200_OK)
            else:
                return Response({"stateCode": 202, "msg": "密码不正确"}, 202)  # 密码不正确
        else:
            return Response({"stateCode": 201, "msg": "用户不存在"}, 201)  # 用户不存在


# 生成商品图片上传的token
class ImgUploadTokenAPIView(APIView):
    def post(self, request, format=None):
        data = request.data
        # username = data.get('username')
        filetype = data.get('filetype')
        timestamp = data.get('timestamp')
        # try:
        #     user = User.objects.get(username__exact=username)
        # except User.DoesNotExist:
        #     user = None
        # user_username = request.session.get('user_username')
        # if username == user_username:
        if request.user.is_authenticated:
            # 构建鉴权对象
            q = Auth(configs.get('qiniu').get('AK'), configs.get('qiniu').get('SK'))

            # 生成图片名
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            # key = salt + '_' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '.' + filetype
            key = salt + '_' + str(int(time.time())) + '.' + filetype

            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(configs.get('qiniu').get('bucket_name'), key, 3600)
            return Response({"stateCode": 200, "token": token, "key": key, "timestamp": timestamp}, 200)
        else:
            return Response({"stateCode": 201, "msg": "您没有权限执行此操作"}, 201)
