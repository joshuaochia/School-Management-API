from rest_framework.exceptions import APIException
from rest_framework import status

class ActionDecor(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error on the server, please comeback later.'
    default_code = 'Error'