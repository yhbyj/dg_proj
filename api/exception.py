# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/10 14:34'

from rest_framework.response import Response
from rest_framework.views import exception_handler \
    as drf_exception_handler


def exception_handler(exc, context):
    # drf做基础处理
    response = drf_exception_handler(exc, context)
    # 为空，自定义二次处理
    if response is None:
        print('{}-{}-{}'.format(
            context['view'],
            context['request'].method,
            exc
        ))
        return Response(
            {
                'detail': '服务器错误'
            }
        )
    return response
