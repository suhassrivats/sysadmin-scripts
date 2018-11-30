##################################################
# This script reads a given password file and writes only email addresses
# to a file
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}, {Project: Get username from a password file}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Mmaintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 get_usernames.py <filepath> <filename>
##################################################

import sys
import os
import subprocess

def main():

    active_users = []
    # Fetch input variables from command line
    filepath = sys.argv[1]
    filename = sys.argv[2]

    # Reads a password file and stores each line in a list names passwords
    with open(filepath, 'r') as f:
        passwords = f.readlines()

        # Iterate through each item in a list
        for password in passwords:
            # Format the line to fetch only username
            username = password.split()[0]

            # Check if an employee is 'Active'
            emp_status_cmd = 'tdph -w -h email=%s return email empcode' % str(username)
            output = subprocess.getoutput(emp_status_cmd)

            # If there is an output and if a user is active, then print and
            # write to a file
            if len(output) > 0:
                user_status = output.split()[1]
                if user_status == 'Active':
                    email = str(username) + '@example.com;'
                    active_users.append(email)
                    print(email)

                    # Write user email address to a file
                    with open(filename, 'a') as f:
                        f.write(email + '\n')


if __name__ == '__main__':
    main()
