# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/10 8:53'

from django.conf import settings
from rest_framework import serializers, exceptions

from api import models


class UserSerializer(serializers.Serializer):
    """用户序列化类"""
    # 非自定义序列化属性
    # 名字一定要与数据库字段相同
    name = serializers.CharField()
    phone = serializers.CharField()
    # sex = serializers.IntegerField()
    # icon = serializers.ImageField()

    # 自定义序列化属性
    # 属性名随意，值由固定的命名规范方法提供：
    # get_属性名(self, 参与序列化的model对象)
    # 返回值是自定义序列化属性的值
    sex = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_sex(self, obj):
        # choice类型的解释型值，get_字段_display()来访问
        return obj.get_sex_display()

    def get_icon(self, obj):
        # obj.icon不能直接作为数据返回，
        # 因为内容虽然是字符串，但是类型是ImageField类型
        return '{}{}{}'.format(
            'http://127.0.0.1:8000',
            settings.MEDIA_URL,
            str(obj.icon)
        )


class UserDeserializer(serializers.Serializer):
    """用户反序列化类"""
    # 1）哪些字段必须反序列化
    # 2）字段都有哪些安全校验
    # 3）哪些字段需要额外提供校验
    # 4）哪些字段存在联合校验
    # 反序列化都是用来入库的，不会出现自定义属性
    # 但会出现可以设置校验规则的自定义属性（如re_pwd）
    name = serializers.CharField(
        max_length=64,
        min_length=3,
        error_messages={
            'max_length': '太长',
            'min_length': '太短'
        }
    )
    pwd = serializers.CharField()
    phone = serializers.CharField(
        required=False
    )
    sex = serializers.IntegerField(
        required=False
    )

    # 自定义有校验规则的反序列化字段
    re_pwd = serializers.CharField(required=True)

    # 局部狗子，validate_要校验的字段名(self, 当前要校验字段的值)
    # 校验规则，校验通过返回原值，校验失败，抛出异常
    def validate_name(self, value):
        # print('value', value)
        if 'j' in value.lower():
            raise exceptions.ValidationError('名字非法，是个鸡贼！')
        return value

    # 全局钩子， validate(self， 系统和局部狗子校验通过的所有数据)
    def validate(self, attrs):
        # print('attrs', attrs)
        pwd = attrs.get('pwd')
        re_pwd = attrs.pop('re_pwd')
        if pwd != re_pwd:
            raise exceptions.ValidationError({'pwd & re_pwd': '两次密码不一致！'})
        return attrs

    # 要完成新增，需要自己重写 create 方法
    def create(self, validated_data):
        # 尽量在所有校验规则完毕后，数据可以直接入库
        # print(validated_data)
        return models.User.objects.create(**validated_data)
