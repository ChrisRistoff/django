'''
Core views for the application.
'''

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health_check(request):
    ''' returns status ok to indicate the application is running '''
    return Response({'status': 'ok'})
