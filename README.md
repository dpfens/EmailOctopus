# EmailOctopus
Python 2/3 Wrapper for the Email Octopus API

## Dependencies

1. requests

## Getting Started
Pass your Email Octopus API key as the argument to `emailoctopus.api.RestAPI`:

```python
from emailoctopus.api import RestAPI
from emailoctopus.campaign import Campaign
api_key = '00000000-0000-0000-0000-000000000000'
api = RestAPI(api_key)
campaigns, paging = Campaign.get(api)
```

### Paging
To fetch the next/previous page when fetching `Campaign` or `EmailList`, :
```python
campaigns = []
current_page = 1
campaign_page_count = float('inf')
while campaign_page_count:
    campaign_page, paging = Campaign.get(api)
    campaigns += campaign_page
    campaign_page_count = len(campaign_page)
    current_page += 1
```

### Campaign reporting
To fetch a `Summary` of a given `Campaign`:
```python
from emailoctopus.campaign import Summary, Report
for campaign in campaigns:
    campaign_summary = Summary.get(api, campaign)
    bounce_report = Report.bounced(api, campaign)
```

To fetch a given

### Fetching Lists
To fetch a List, use the `emailoctopus.email_list.EmailList` class:
```python
from emailoctopus.email_list import EmailList
email_lists, paging = EmailList.get(api)
```

### Creating a List
```python
email_list_instance = EmailList.create(api, 'My New List')
```

### Deleting a List
```python
email_list_instance.delete(api)
```

### Fetching Contacts
To fetch the `Contacts` of a given `EmailList`:
```python
from emailoctopus.email_list import Contact
for email_list in email_lists:
    list_contacts = Contact.get(api, email_list)
```

### Adding a person as a Contact to a List
```python
fields = dict(FirstName='John', LastName='Doe')
status = 'SUBSCRIBED'
new_contact_instance = Contact.create(api, email_list_instance, 'johndoe@email.com', fields, status=status)
```
