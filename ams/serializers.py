#coding:utf-8
from ams.models import AppComment, VersionManager
from rest_framework import serializers


class AppCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppComment


class VersionManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersionManager
        fields = ['version_code','version_name','description','download_url']
