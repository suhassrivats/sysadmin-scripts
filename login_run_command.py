##################################################
# This script reads hostlist from a file and executes a command in the remote
# server
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Mmaintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 login_run_command.py
##################################################

import subprocess
import os

with open('hostlist', 'r') as h:
    for server in h:
        cmd = "rsh %s uptime" % str(server).strip()
        output = subprocess.getoutput(cmd).strip('\n').split('\n')
        output_string = str(server.strip()), str(output[-1])
        output_string = str(output_string)[1:-1].replace("'", "")
        print(output_string)

        with open('hostlist_output', 'a') as ho:
            ho.write(str(output_string)+'\n')
