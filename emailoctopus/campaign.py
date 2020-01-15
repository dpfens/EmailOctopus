import logging
from . import email_list
from datetime import datetime

logger = logging.getLogger(__name__)


class Campaign(object):
    __slots__ = ('id', 'status', 'name', 'subject', 'to', 'sender', 'content', 'created_at', 'sent_at')
    datetime_format = '%Y-%m-%dT%H:%M:%S+00:00'

    def __init__(self, id, status, name, subject, to, sender, content, created_at, sent_at):
        self.id = id
        self.status = status
        self.name = name
        self.subject = subject
        self.to = to
        self.sender = sender
        self.content = content
        self.created_at = created_at
        self.sent_at = sent_at

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<%s %s id=%r, name=%r, status=%r>' % (self.__class__.__name__, id(self), self.id, self.name, self.status)

    @classmethod
    def from_api(cls, data):
        id = data['id']
        status = data['status']
        name = data['name']
        subject = data['subject']
        to = data['to']
        sender = data['from']
        content = data['content']
        created_at = data['created_at']
        created_at = datetime.strptime(created_at, cls.datetime_format)
        sent_at = data['sent_at']
        if sent_at:
            sent_at = datetime.strptime(sent_at, cls.datetime_format)
        return cls(id, status, name, subject, to, sender, content, created_at, sent_at)

    @classmethod
    def get(cls, api, campaign_id=None, **kwargs):
        if campaign_id:
            path = 'campaigns/%s' % campaign_id
            response = api._request(path)
            output = cls.from_api(response)
        else:
            limit = kwargs.get('limit', 100)
            page = kwargs.get('page', 1)
            params = dict(limit=limit, page=page)
            path = 'campaigns'
            response = api._request(path, params=params)
            instances = [cls.from_api(row) for row in response.get('data', [])]
            paging_data = response.get('paging', dict())
            output = instances, paging_data
        return output


class Summary(object):
    __slots__ = ('id', 'sent', 'bounced', 'opened', 'clicked', 'complained', 'unsubscribed')
    datetime_format = '%Y-%m-%dT%H:%M:%S%z'

    def __init__(self, id, sent, bounced, opened, clicked, complained, unsubscribed):
        self.id = id
        self.sent = sent
        self.bounced = bounced
        self.opened = opened
        self.clicked = clicked
        self.complained = complained
        self.unsubscribed = unsubscribed

    def __str__(self):
        return str(self.id)

    @classmethod
    def from_api(cls, data):
        return cls(**data)

    @classmethod
    def get(cls, api, campaign):
        path = 'campaigns/%s/reports/summary' % campaign
        response = api.request(path)
        return cls.from_api(response)


class Report(object):
    __slots__ = ('data', 'paging')
    datetime_format = '%Y-%m-%dT%H:%M:%S%z'

    def __init__(self, data, paging):
        self.data = data
        self.paging = paging

    def __iter__(self):
        for item in self.data:
            yield dict(**item)

    @classmethod
    def from_api(cls, data):
        all_contact_data = data['data']
        contact_count = len(all_contact_data)
        for i in range(contact_count):
            row = contact_data[i]
            contact_data = row['contact']
            all_contact_data[i]['contact'] = email_list.Contact.from_api(contact_data)
            occurred_at = row.get('occurred_at')
            if occurred_at:
                all_contact_data[i]['occurred_at'] = datetime.strptime(occurred_at, cls.datetime_format)

    @classmethod
    def bounced(cls, api, campaign):
        path = 'campaigns/%s/reports/bounced' % campaign
        response = api.request(path)
        return cls.from_api(response)

    @classmethod
    def clicked(cls, api, campaign):
        path = 'campaigns/%s/reports/clicked' % campaign
        response = api.request(path)
        return cls.from_api(response)

    @classmethod
    def complained(cls, api, campaign):
        path = 'campaigns/%s/reports/complained' % campaign
        response = api.request(path)
        return cls.from_api(response)

    @classmethod
    def opened(cls, api, campaign):
        path = 'campaigns/%s/reports/opened' % campaign
        response = api.request(path)
        return cls.from_api(response)

    @classmethod
    def sent(cls, api, campaign):
        path = 'campaigns/%s/reports/sent' % campaign
        response = api.request(path)
        return cls.from_api(response)

    @classmethod
    def unsubscribed(cls, api, campaign):
        path = 'campaigns/%s/reports/unsubscribed' % campaign
        response = api.request(path)
        return cls.from_api(response)

    @classmethod
    def not_clicked(cls, api, campaign):
        path = 'campaigns/%s/reports/not-clicked' % campaign
        response = api.request(path)
        return cls.from_api(response)

    @classmethod
    def not_opened(cls, api, campaign):
        path = 'campaigns/%s/reports/not-opened' % campaign
        response = api.request(path)
        return cls.from_api(response)
