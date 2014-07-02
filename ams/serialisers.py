#coding:utf-8
from ams.models import AppComment
from rest_framework import serializers

class AppCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppComment
