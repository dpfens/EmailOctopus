if __name__ == '__main__':
    import argparse
    from emailoctopus.api import RestAPI
    from emailoctopus.campaign import Campaign, Report
    from emailoctopus.email_list import EmailList

    parser = argparse.ArgumentParser(description='Test a connection to the Email Octopus API')
    parser.add_argument('-a', '--api_key', required=True, type=str, help='The api_key to use to authenticate')
    args = parser.parse_args()

    api = RestAPI(args.api_key)
    email_lists, paging = EmailList.get(api)


    campaigns, paging = Campaign.get(api)
    print(campaigns)
