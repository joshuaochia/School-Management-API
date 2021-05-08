
from rest_framework.views import exception_handler



def _handle_authentication_error(exc, context, response):
    
    response.data = {
        'error': 'Please log in to proceed'
    }

    return response


def _handle_permission_error(exc, context, response):

    response.data = {
        'Permission error': "You don't have any permission to access this"
    }

    return response

def _handle_http404_error(exc, context, response):

    response.data = {
        'No url found': "This url doesn't exist"
    }

    return response

def _handle_generic_error(exc, context, response):

    response.data = {
        'error': 'Not validated'
    }
    return response

def _handle_method_error(exc, context, response):

    response.data = {
        'Method': 'Not allowed'
    }

    return response

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError': _handle_generic_error,
        'HTTP404': _handle_http404_error,
        'PermissionDenied': _handle_permission_error,
        'NotAuthenticated': _handle_authentication_error,
        'MethodNotAllowed': _handle_method_error,
    }

    response = exception_handler(exc, context)
    

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    
    if response is not None:
        response.data['status_code'] = response.status_code
    
    return response
