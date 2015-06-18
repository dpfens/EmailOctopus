import requests
from models import *

SUPPORTED_FORMATS = ['json']

class EmailOctopusAPI(object):
    protocol = 'https://'
    host = 'emailoctopus.com'
    path = '/api/1/'
    lists = 'lists'
    list_members = '/members'
    list_url = protocol + host + path + lists
    
    def __init__(self, key, **kwargs):
        self.key = key
        format = kwargs.get('format', 'json')
        if format in SUPPORTED_FORMATS:
            self.format = format
    
    # Lists 
    def get_lists(self):
        payload = {"api_key": self.key }
        request = requests.get(EmailOctopusAPI.list_url, params=payload)
        response = request.json()
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return [EOList.from_dict(i) for i in response['lists'] ]
    
    def get_list(self, id):
        url = EmailOctopusAPI.list_url +'/'+id
        payload = {"api_key": self.key }
        request = requests.get(url, params=payload)
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return EOList.from_dict(response['list'])
    
    def create_list(self, name):
        payload = {"api_key": self.key, "name":name }
        request = requests.post(EmailOctopusAPI.list_url, params=payload)
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return EOList.from_dict(response['list'])
    
    def update_list(self, id, name):
        url = EmailOctopusAPI.list_url+'/'+id
        payload = {"api_key": self.key, "name":name }
        request = requests.put(list_url+'/'+id, params=payload)
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return EOList.from_dict(response['list'])
    
    def delete_list(self, id):
        url = EmailOctopusAPI.list_url+'/'+id
        payload = {"api_key": self.key }
        request = requests.delete(EmailOctopusAPI.list_url, params=payload)
        response = request.json()
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return response
    
    # List Members
    def get_list_member(self, list_id, member_id):
        url = EmailOctopusAPI.list_url+'/'+list_id+EmailOctopusAPI.list_members+'/'+member_id
        payload = {"api_key": self.key}
        request = requests.get(url, params=payload)
        response = request.json()
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return EOListMember.from_dict(response)
    
    def get_list_members(self, list_id):
        url = EmailOctopusAPI.list_url+'/'+list_id+EmailOctopusAPI.list_members
        payload = {"api_key": self.key}
        request = requests.get(url, params=payload)
        response = request.json()
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return [EOListMember.from_dict(i)  for i in response['members']]
    
    def create_list_member(self, list_id, payload):
        url = EmailOctopusAPI.list_url+'/'+list_id+EmailOctopusAPI.list_members
        payload["api_key"] = self.key
        request = requests.post(url, params=payload)
        response = request.json()
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return EOListMember.from_dict(response)
    
    def update_list_member(self, list_id, member_id, payload):
        url = EmailOctopusAPI.list_url+'/'+list_id+EmailOctopusAPI.list_members +'/' + member_id
        payload["api_key"] = self.key
        request = requests.put(url, params=payload)
        response = request.json()
        print(url)
        print(response)
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return EOListMember.from_dict(response)
    
    def delete_list_member(self, list_id, member_id):
        url = EmailOctopusAPI.list_url+'/'+list_id+EmailOctopusAPI.list_members +'/' + member_id
        payload = {"api_key": self.key }
        request = requests.delete(url, params=payload)
        response = request.json()
        if request.status_code != requests.codes.ok:
            raise EmailOctopusClientException(response['error']['message'], response['error']['code'])
        return response