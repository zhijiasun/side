from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ams.models import AppComment, VersionManager
from ams.serializers import VersionManagerSerializer

import logging
logger = logging.getLogger(__name__)
# Create your views here.


@api_view(['POST'])
def submit_comment(request):
    if request.method == 'POST':
        result = {'errCode':10000,'errDesc':'submit comment successfully'}
        content = request.DATA.get('comment', '')
        if content:
            c = AppComment.objects.create(app_content=content)
            c.save()
            return Response(result, status=status.HTTP_200_OK)
        else:
            logger.debug('comment is NULL')
            result['errCode'] = 10012
            result['errDesc'] = 'comment is NULL'
            return Response(result,status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_version(request):
    result = {'errCode':10012, 'errDesc':'no version info exist', 'data':{}}
    try:
        version = VersionManager.objects.latest('version_id')
        if version:
            vs = VersionManagerSerializer(version)
            result = {'errCode':10000,'errDesc':'retrive version successfully','data':vs.data}
    except:
        print('version info not exist')
        logger.debug('version info not exist')

    return Response(result, status=status.HTTP_200_OK)
