import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class EmailList(object):
    __slots__ = ('id', 'name', 'double_opt_in', 'fields', 'counts', 'created_at')
    datetime_format = '%Y-%m-%dT%H:%M:%S+00:00'

    def __init__(self, id, name, double_opt_in, fields, counts, created_at):
        self.id = id
        self.name = name
        self.double_opt_in = double_opt_in
        self.fields = fields
        self.counts = counts
        self.created_at = created_at

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        unsubscribed = self.counts['unsubscribed']
        pending = self.counts['pending']
        subscribed = self.counts['subscribed']
        return '<%s %s id=%r, name=%r, unsubscribed=%r, pending=%r, subscribed=%r, fields=%r, created_at=%s>' % (self.__class__.__name__, id(self), self.id, self.name, unsubscribed, pending, subscribed, self.fields, self.created_at)

    @classmethod
    def from_api(cls, data):
        created_at = data['created_at']
        data['fields'] = [ListField.from_api(field) for field in data['fields']]
        data['created_at'] = datetime.strptime(created_at, cls.datetime_format)
        return cls(**data)

    def update(self, api):
        path = 'lists/%s' % self.id
        params = dict(name=self.name)
        api.request(path, params=params, method='PUT')

    def delete(self, api):
        path = 'lists/%s' % self.id
        api.request(path, method='DELETE')

    @classmethod
    def get(cls, api, **kwargs):
        list_id = kwargs.get('list_id')
        if list_id:
            path = 'lists/%s' % list_id
            response = api.request(path)
        else:
            limit = kwargs.get('limit', 100)
            page = kwargs.get('page', 1)
            params = dict(limit=limit, page=page)
            path = 'lists'
            response = api.request(path, params=params)
            instances = [cls.from_api(item) for item in response.get('data', [])]
            paging_data = response.get('paging', dict())
            output = instances, paging_data
        return output

    @classmethod
    def create(cls, api, name):
        path = 'lists'
        params = dict(name=name)
        response = api.request(path, params=params, method='POST')
        return cls.from_api(response)


class Contact(object):
    __slots__ = ('id', 'email_address', 'fields', 'status', 'created_at')
    datetime_format = '%Y-%m-%dT%H:%M:%S%z'

    def __init__(self, id, email_address, fields, status, created_at):
        self.id = id
        self.email_address = email_address
        self.fields = fields
        self.status = status
        self.created_at = created_at

    def __str__(self):
        return str(self.id)

    def update(self, api, email_list):
        path = 'lists/%s/contacts/%s' % (email_list, self.id)
        params = dict(email_address=self.email_address, fields=self.fields, status=self.status)
        api.request(path, params=params, method='PUT')

    def delete(self, api, email_list):
        path = 'lists/%s/contacts/%s' % (email_list, self.id)
        api.request(path, method='DELETE')

    @classmethod
    def from_api(cls, data):
        id = data['id']
        email_address = data['email_address']
        fields = data['fields']
        status = data['status']
        created_at = data['created_at']
        created_at = datetime.strptime(created_at, cls.datetime_format)
        return cls(id, email_address, fields, status, created_at)

    @classmethod
    def get(cls, api, email_list, **kwargs):
        contact = kwargs.get('contact')
        if contact:
            path = 'lists/%s/contacts/%s' % (email_list, contact)
            response = api.request(path)
            output = cls.from_api(response)
        else:
            limit = kwargs.get('limit', 100)
            page = kwargs.get('page', 1)
            params = dict(limit=limit, page=page)
            path = 'lists/%s/contacts' % email_list
            response = api.request(path, params=params)
            instances = [cls.from_api(item) for item in response.get('data', [])]
            paging_data = response.get('paging', dict())
            output = instances, paging_data
        return output

    @classmethod
    def create(cls, api, email_list, email_address, **kwargs):
        fields = kwargs.get('fields', dict())
        status = kwargs.get('status', 'PENDING')
        path = 'lists/%s/contacts' % email_list
        params = dict(email_address=email_address, fields=fields, status=status)
        response = api.request(path, params=params, method='POST')
        return cls.from_api(response)

    @classmethod
    def subscribed(cls, api, email_list, **kwargs):
        limit = kwargs.get('limit', 100)
        page = kwargs.get('page', 1)
        path = 'lists/%s/contacts/subscribed' % email_list
        params = dict(limit=limit, page=page)
        response = api.request(path, params=params)
        return [cls.from_api(item) for item in response.get('data', [])]

    @classmethod
    def unsubscribed(cls, api, email_list, **kwargs):
        limit = kwargs.get('limit', 100)
        page = kwargs.get('page', 1)
        path = 'lists/%s/contacts/unsubscribed' % email_list
        params = dict(limit=limit, page=page)
        response = api.request(path, params=params)
        return [cls.from_api(item) for item in response.get('data', [])]


class ListField(object):
    __slots__ = ('tag', 'type', 'label', 'fallback')

    def __init__(self, tag, type, label, fallback):
        self.tag = tag
        self.type = type
        self.label = label
        self.fallback = fallback

    def __str__(self):
        return str(self.tag)

    def __repr__(self):
        return '<%s %s label=%r, tag=%r type=%r>' % (self.__class__.__name__, id(self), self.label, self.tag, self.type)

    def update(self, api, email_list):
        path = 'lists/%s/fields' % (email_list, self.tag)
        params = dict(label=self.label, tag=self.tag, type=self.type, fallback=self.fallback)
        api.request(path, params=params, method='PUT')

    def delete(self, api, email_list):
        path = 'lists/%s/fields' % (email_list, self.tag)
        api.request(path, method='DELETE')

    @classmethod
    def from_api(cls, data):
        tag = data['tag']
        type = data['type']
        label = data['label']
        fallback = data['fallback']
        return cls(tag, type, label, fallback)

    @classmethod
    def create(cls, api, email_list, label, tag, type, fallback=None):
        path = 'lists/%s/fields' % (email_list, tag)
        params = dict(label=label, tag=tag, type=type, fallback=fallback)
        response = api.request(path, params=params, method='POST')
        return cls.from_api(response)
