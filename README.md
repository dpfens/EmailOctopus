# EmailOctopusAPI
Python 2.7 wrapper for Email Octopus
Email Octopus API
=================

This is a simple API wrapper for Python 2.7 and below.  It provides simple access to  lists and list members.

Dependencies
-----

1.  requests

Getting Started
-----

It is not difficult. pass your Email Octopus API key as the argument to `client.EmailOctopusAPI` and you can start making calls to the API.

>   import client
>   api = client.EmailOctopusAPI('00000000-0000-0000-0000-000000000000')

Classes
-----

The wrapper returns instances of these classes. If accessing the List API, all lists will be returned as instances of `EOList`.  If accessing a List Member API, an `EOListMember` instance will be returned.

-EOList
  -id
  -name
  -created_at
-EOListMember
  -id
  -first_name
  -last_name
  -email_address
  -subscribed
  -created_at
  
API Methods
-----
-List
  -`get_lists()`
  -`get_list(id)`
  -`create_list(name)`
  -`update_list(name)`
  -`delete_list(id)`

-List Member
  -`get_list_members(list_id)`
  -`get_list_member(list_id, member_id)`
  -`create_list_member(list_id, data)`
  -`update_list_member(list_id, member_id, data)`
  -`delete_list_member(list_id, member_id)`
