#coding:utf-8
from ams.models import AppComment, VersionManager
from rest_framework import serializers


class AppCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppComment


class VersionManagerSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField('str_download_url')
    class Meta:
        model = VersionManager
        fields = ['version_code','version_name','description','download_url']

    def str_download_url(self,obj):
        if obj.download_url:
            return obj.download_url.url
