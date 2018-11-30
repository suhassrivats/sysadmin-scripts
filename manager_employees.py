##################################################
# A script to list all employees under a manager. Make a rest API call to 
# search by a manager and pull all his employees. Fetch the response of an API 
# call and display only usernames employees.
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}, {Project: Manager's employee list}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Mmaintainer: {suhas srivats}
# Email: {email_address}
# Status: {dev_status}
# Example: python manager_employees.py <manager-name>
##################################################

import sys
import json
import argparse
import requests
requests.packages.urllib3.disable_warnings()


def main():
    usernames = []

    # Argparse Command Line
    parser = argparse.ArgumentParser(
        description='A script to find all employees under a manager')
    parser.add_argument(
        'manager', help='Enter the name of a manager here')
    args = parser.parse_args()

    # Make an API call
    headers = {
        'Authorization': 'Basic token=YOUR-TOKEN',
    }
    params = (
        ('management_chain', args.manager),
        ('match', 'like'),
    )

    # Results are stored in response variable
    response = requests.get('https://lookup.example.com/api/search/findby',
                            headers=headers, params=params, verify=False)

    # Execute the script if there is a response. Exit otherwise.
    if response:
        # Store response.text as JSON
        d = json.loads(response.text)

        # User data is a list of dictionaries with user attributes as each item
        user_data = d['data']
        # print user_data

        # Iterate through every item in a list and write username to a file
        with open(args.manager + '.txt', 'w') as f:
            print 'Data collection in progress..'
            for i in range(len(user_data)):
                username = user_data[i]['person']['username']
                if username:
                    usernames.append(username)
                    f.write(username + '\n')
            print 'Data collection is complete'

    else:
        sys.exit()


if __name__ == '__main__':
    main()
