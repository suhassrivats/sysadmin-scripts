##################################################
# This script runs a particular command on a server and prints its output
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Mmaintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 get_command_output.py
##################################################

import sys
import os
import subprocess

with open('inactive_hosts_intel', 'r') as hosts:
    for host in hosts:
        # Run ypcat command on a server
        cmd = "ypcat hosts |grep %s" % str(host).strip('\n')
        # output = subprocess.getoutput(cmd)
        output = subprocess.getoutput(cmd)
        if output:
            print(host.strip('\n'))
