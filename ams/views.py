from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ams.models import AppComment, VersionManager
from ams.serializers import VersionManagerSerializer
from epm.error import errMsg

import logging
logger = logging.getLogger(__name__)
# Create your views here.


@api_view(['POST'])
def submit_comment(request):
    if request.method == 'POST':
        result = {'errCode':10000,'errDesc':errMsg[10000]}
        comment = request.DATA.get('comment', '')
        version = request.DATA.get('app_version', '')
        info = request.DATA.get('phone_info', '')
        if comment and version and info:
            c = AppComment.objects.create(comment=comment, app_version=version, phone_info = info)
            c.save()
            return Response(result, status=status.HTTP_200_OK)
        else:
            logger.debug('comment is NULL')
            result['errCode'] = 10007
            result['errDesc'] = errMsg[10007]
            return Response(result,status = status.HTTP_200_OK)


@api_view(['GET'])
def get_version(request):
    result = {'errCode':10000, 'errDesc':errMsg[10000]}
    try:
        versions = VersionManager.objects.filter(specified_app=0).order_by('-version_id')
        if versions:
            vs = VersionManagerSerializer(versions[0])
            result['data']=vs.data
    except Exception,e:
        print str(e)
        logger.debug('version info not exist')

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_worker_version(request):
    result = {'errCode':10000, 'errDesc':errMsg[10000]}
    try:
        versions = VersionManager.objects.filter(specified_app=1).order_by('-version_id')
        if versions:
            vs = VersionManagerSerializer(versions[0])
            result['data']=vs.data
    except:
        print('version info not exist')
        logger.debug('version info not exist')

    return Response(result, status=status.HTTP_200_OK)
