from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models, serializers


class Book(APIView):
    """图书类"""
    # 局部解析类配置
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Book.objects.get(pk=pk)
            return Response(
                {
                    'status': 0,
                    'msg': 'ok',
                    'results': {
                        'title': book_obj.title,
                        'price': book_obj.price
                    }
                }
            )
        return Response('get ok')

    def post(self, request, *args, **kwargs):
        # url拼接参数：只有一中传参方式就是拼接参数
        print(request.query_params)
        # 数据包传参，有三种传参方式：form-data, urlencoding, json
        print(request.data)
        return Response('post ok')


class User(APIView):
    """用户类"""

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                # 用户对象不能直接作为数据返回给前台
                user_obj = models.User.objects.get(pk=pk)
                # 序列化一下用户对象
                user_ser = serializers.UserSerializer(
                    user_obj
                )
                return Response(
                    {
                        'status': 0,
                        'msg': 'ok',
                        'results': user_ser.data
                    }
                )
            except:
                return Response(
                    {
                        'status': 2,
                        'msg': '用户不存在'
                    }
                )
        else:
            # 用户对象列表(queryset)不能直接作为数据返回给前台
            user_obj_list = models.User.objects.all()
            # 序列化一下用户对象
            user_ser = serializers.UserSerializer(
                user_obj_list,
                many=True
            )
            return Response(
                {
                    'status': 0,
                    'msg': 'ok',
                    'results': user_ser.data
                }
            )

    # 只考虑单增
    def post(self, request, *args, **kwargs):
        request_data = request.data
        # 数据是否合法（增加对象需要一个字典数据）
        if not isinstance(request_data, dict) or request_data == {}:
            return Response(
                {
                    'status': 1,
                    'msg': '数据有误'
                }
            )
        # 数据类型合法，但数据内容不一定合法，需要校验数据
        user_ser = serializers.UserDeserializer(data=request_data)
        if user_ser.is_valid():
            # 校验通过，完成新增
            user_obj = user_ser.save()
            # print('user_obj', user_obj)
            return Response(
                {
                    'status': 0,
                    'msg': 'ok',
                    'results': serializers.UserSerializer(
                        user_obj
                    ).data
                    # 'results': ''
                }
            )
        else:
            # 校验失败
            return Response(
                {
                    'status': 1,
                    'msg': user_ser.errors
                }
            )
