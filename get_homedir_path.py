##################################################
# Get symlink path of a user by looking at /remote/home/<user> and create
# a link in /cherry/cherryu/<user>
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Maintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 get_homedir_path.py
# Shebang: #!/depot/python/bin/python
##################################################

import os
import subprocess


def main():
    # Command to get all valid users
    cmd = "ypcat passwd |awk -F ':' '!/no_ip_cert/ {print $1}'"
    output = subprocess.getoutput(cmd)

    users = (output.split('\n'))

    with open('homedirinfo.txt', 'w') as f:
        for user in users:
            # Make sure there are NO sudo accounts. They start with uppercase
            if not user[0].isupper():
                snps_homedir = os.path.realpath('/remote/home/%s' % user)
                cherryu_homedir = '/cherry/cherryu/%s' % user
                write_string = 'ln -s %s %s \n' % (snps_homedir,
                                                   cherryu_homedir)
                f.write(write_string)


if __name__ == '__main__':
    main()
