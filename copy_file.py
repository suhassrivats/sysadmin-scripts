##################################################
# This script copies a file from one server to a list of servers
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}, {Project: Copy file from one server to another}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Mmaintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python2.6 copy_file.py
##################################################

import subprocess
import os

# Open a file with a list of servers
with open('/tmp/servers.txt', 'r') as servers:
    for server in servers:
        # Login to each server
        server_path = 'root@' + str(server).strip('\r\n') + ':/root/'
        # Copy that file to '/root/.rhosts' location in the destination server
        p = subprocess.Popen(["scp", "/tmp/.rhosts", server_path])
        sts = os.waitpid(p.pid, 0)
