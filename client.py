import requests, re
from models import *

SUPPORTED_FORMATS = ['json']

def encode_string(value):
    return value.encode('utf-8') \
        if isinstance(value, six.text_type) else str(value)

class EmailOctopusAPI(object):
    protocol = 'https://'
    host = 'emailoctopus.com'
    path = '/api/1/'
    lists = 'lists'
    list_members = '/members'
    api_url = protocol+host+path
    
    def __init__(self, key, **kwargs):
        self.key = key
        format = kwargs.get('format', 'json')
        if format in SUPPORTED_FORMATS:
            self.format = format
            
    def _request(self, **config):
        method_type = config.get('method', 'get').lower()
        method = getattr(requests, method_type)
        route = EmailOctopusAPI.api_url + config.get('route',  EmailOctopusAPI.lists)
        parameters = re.findall('\{\w+\}',route)
        params = config.get('payload', {})
        data = config.get('data', {})
        
        if parameters:
            for param in parameters:
                name = param.strip('{}')
                if not name in config:
                    raise EmailOctopusClientException('INVALID PARAMETERS', 'Parameters are missing or invalid')
                value = config[name]
                route = route.replace(param, value)
        
        if method_type == 'post':
            data["api_key"] = self.key
        else:
            params["api_key"] = self.key
        
        request = method(route, params=params, data=data)
        response = request.json()
        if request.status_code != requests.codes.ok:
            raise EmailOctopusAPIException(response['error']['message'], response['error']['code'])
        return response
    
    # Lists 
    def get_lists(self):
        response = self._request(method='GET', route='lists')
        return [EOList.from_dict(i) for i in response['lists'] ]
    
    def get_list(self, id):
        response = self._request(method='GET', route='lists/{list_id}', list_id=id)
        return EOList.from_dict(response)
    
    def create_list(self, name):
        response = self._request(method='POST', route='lists', data={"name":name})
        return EOList.from_dict(response)
    
    def update_list(self, id, name):
        response = self._request(method='PUT', route='lists/{list_id}', list_id=id, data={"name":name})
        return EOList.from_dict(response)
    
    def delete_list(self, id):
        response = self._request(method='DELETE', route='lists/{list_id}', list_id=id)
        return response
    
    # List Members
    def get_list_member(self, list_id, member_id):
        response = self._request(method='GET', route='lists/{list_id}/members/{member_id}', list_id=list_id, member_id=member_id)
        return EOListMember.from_dict(response)
    
    def get_list_members(self, list_id):
        response = self._request(method='GET', route='lists/{list_id}/members', list_id=list_id)
        return [EOListMember.from_dict(i)  for i in response['members']]
    
    def create_list_member(self, list_id, data):
        response = self._request(method='POST', route='lists/{list_id}/members', list_id=list_id, data=data)
        return EOListMember.from_dict(response)
    
    def update_list_member(self, list_id, member_id, data):
        response = self._request(method='PUT', route='lists/{list_id}/members/{member_id}', list_id=list_id, member_id=member_id, data=data)
        return EOListMember.from_dict(response)
    
    def delete_list_member(self, list_id, member_id):
        response = self._request(method='DELETE', route='lists/{list_id}/members/{member_id}', list_id=list_id, member_id=member_id)
        return response