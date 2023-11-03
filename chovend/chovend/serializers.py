from rest_framework import serializers
from typing import Optional, Dict

class ErrorResponseSerializer(serializers.Serializer):
    # code = serializers.CharField(default='E00')
    message = serializers.CharField(default='An error has occured!')
    data = serializers.DictField(allow_empty=True, default={})
    # status = serializers.BooleanField(default=False)


class SuccessResponseSerializer(serializers.Serializer):
    # code = serializers.CharField(default='01')
    message = serializers.CharField(default='Success!')
    data = serializers.DictField(allow_empty=True, default={})
    # status = serializers.BooleanField(default=True)