import logging
import requests
from . import exception


logger = logging.getLogger(__name__)


class RestAPI(object):
    __slots__ = ('api_key', 'endpoint')

    def __init__(self, api_key, **kwargs):
        self.api_key = api_key
        self.endpoint = kwargs.get('endpoint', 'https://emailoctopus.com/api')

    def _request(self, path, **kwargs):
        version = kwargs.get('version', '1.5')
        kwargs = dict(**kwargs)
        method = kwargs.pop('method', 'GET')
        params = dict(**kwargs.get('params', dict()))

        if kwargs.pop('full', False):
            url = path
        else:
            url = '%s/%s/%s' % (self.endpoint, version, path)
        params['api_key'] = self.api_key
        kwargs['params'] = params

        logger.debug('URL: %r, %r', url, kwargs)
        response = requests.request(method, url, **kwargs)
        response_data = response.json()
        if 'code' in response_data:
            code = response_data['code']
            message = response_data['message']
            exception_cls = exception.EmailOctopusException
            if code == exception.InvalidParametersException.error_code:
                exception_cls = exception.InvalidParametersException
            elif code == exception.InvalidKeyException.error_code:
                exception_cls = exception.InvalidKeyException
            elif code == exception.UnauthorisedException.error_code:
                exception_cls = exception.UnauthorisedException
            elif code == exception.NotFoundException.error_code:
                exception_cls = exception.NotFoundException
            raise exception_cls(code=code, message=message)
        return response_data

    def request(self, path, **kwargs):
        return self._request(path, **kwargs)
