##################################################
# Creates a home directory for a new user, change the permissions and link it
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Maintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 new_users_homedir.py
# Shebang: #!/depot/python/bin/python
##################################################

import os
import sys
import errno
import logging
import datetime
import subprocess

# Global variables
current_date = datetime.datetime.now().strftime("%-m/%-d/%Y")
currentDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_users():
    '''
    Parse USERS_file.txt and a list of unique, newly added users by
    comparing the date column in the USERS_file.txt file against server's currentDT date

    Args: none

    Raises:
        IOError: No file available

    Returns:
        uniq_users (list) : A list of current uniqe users
    '''

    users = []

    try:
        with open('/path/USERS_file.txt', 'r') as f:
            lines = f.readlines()

        if len(lines) > 0:
            for line in lines:
                runda_date = (line.strip().split(',')[2].split()[0])
                if current_date == runda_date:
                    new_users = (line.strip().split(',')[-1].strip().
                                 split(':'))
                    if len(new_users) > 0:
                        for user in new_users:
                            users.append(''.
                                         join(e for e in user if e.isalnum()))

            # A list of unique users
            uniq_users = list(set(users))
            # print(uniq_users)
            # print(len(uniq_users))

            return uniq_users

        else:
            logging.info("%s::File is empty" % (currentDT))

    except IOError as e:
        logging.info("%s::Unable to open USERS_file.txt file" % (currentDT))


def check_usr_homedir_snps(users):
    '''
    Check for user's home directory link in /cherry/cherryu/. If symbolic link
    exists, then take no action. If link doesn't exist, then call a function
    which creates home directory.

    Args:
        users (list): A list of current unique users

    Returns: none
    '''

    for user in users:
        path = '/cherry/cherryu/%s' % user

        # Check if a symbolic link exists
        link = os.path.islink(path)
        if link:
            # print("A symbolic link already exists! %s -> %s" %
            #       (path, os.readlink(path)))
            logging.info("%s::A symbolic link already exists for: %s " %
                         (currentDT, path))

        else:
            create_homedir(user)


def create_homedir(user):
    '''
    Creates a user's home directory, updates permissions and creates a
    symbolic link.

    Args:
        user (str): Username

    Raises:
        Exit the program if yplatest (passwd) file is empty

    Returns:
        home directory (file): Home directory of a user
    '''

    try:
        # Dynamically fetch uid and gid from another password file
        with open('/path/yplatest', 'r') as f:
            lines = f.readlines()

        if len(lines) > 0:
            # Get all matching entries for user. Example suhas, suhasb etc
            matching = [line for line in lines if user in line]

            # Make sure that is the exact user
            for entry in matching:
                if user == entry.strip().split(':')[0]:
                    uid = int(entry.strip().split(':')[2])
                    gid = int(entry.strip().split(':')[3])
                    # print(user, uid, gid)
                    logging.info("%s::%s::%s::%s" %
                                 (currentDT, user, uid, gid))

        else:
            logging.info("%s:: yplatest file is empty" % (currentDT))
            # print('yplatest file empty.')
            sys.exit()

        # Create a homedir if it does not exist
        src_dir_name = '/cherry/cherryhome/%s' % user
        dst_dir_name = '/cherry/cherryu/%s' % user

        if not os.path.exists(src_dir_name):
            os.mkdir(src_dir_name)
            # print("Directory ", src_dir_name,  " Created ")
            logging.info("%s::Directory %s is created " %
                         (currentDT, src_dir_name))
        else:
            # print("Directory ", src_dir_name,  " already exists")
            logging.info("%s::Directory %s already exists" %
                         (currentDT, src_dir_name))

        # Chmod 755
        os.chmod(src_dir_name, 0o755)
        logging.info("%s Permissions are changed to 755 for %s" %
                     (currentDT, src_dir_name))

        # Change ownership of the directory
        os.chown(src_dir_name, uid, gid)
        # print('permissions are created')
        logging.info("%s::Directory ownership permissions created for %s" %
                     (currentDT, src_dir_name))

        # Create a symbolic link
        os.symlink(src_dir_name, dst_dir_name)
        logging.info("%s::symbolic link is created %s -> %s" %
                     (currentDT, src_dir_name, dst_dir_name))
        # print('symbolic link is created')

    except IOError as e:
        logging.info("%s::Unable to open yplatest file" % (currentDT))


def main():
    # Create a logging file and update it
    logging.basicConfig(
        filename='/path/user_homedir_addition.log', level=logging.DEBUG)

    # Get a list of newly added unique users
    users = get_users()

    # Check if a user's homedirectory already exists in snps i.e, if not /cherry
    # If it does not exist, create one.
    check_usr_homedir_snps(users)


if __name__ == '__main__':
    main()
