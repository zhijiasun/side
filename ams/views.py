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
    version = VersionManager.objects.latest('version_id')
    vs = VersionManagerSerializer(version)
    result = {'errCode':10000,'errDesc':'retrive version successfully','data':vs.data}
    return Response(result, status=status.HTTP_200_OK)
