#!/depot/python/bin/python

##################################################
# Check if Ansible is installed on a server or not.
# If not, report the error
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {major}.{minor}.{rel}
# Maintainer: {Suhas Srivats}
# Email: {xxx@xxx.com}
# Status: {dev}
# Example: python3 ansible_checker.py
# Shebang: #!/depot/python/bin/python
##################################################

import os
import re
import subprocess


def main():

    # Error log file location
    error_log_file = '/remote/kickstart/log/HOSTNAME/log/action184.log'

    # Open the ansible_status file
    with open('ansible_status.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip().split(':')
        hostname = line[0]
        run_status = line[1].split()
        scm_run_status = re.sub('[^A-Za-z]+', '', run_status[0].split('=')[1])
        ansible_run_status = re.sub('[^A-Za-z]+', '',
                                    run_status[1].split('=')[1])
        new_err_log_file = error_log_file.replace('HOSTNAME', hostname)

        # Check if the machine is up
        cmd = "ping -c 1 %s" % hostname
        output = subprocess.getoutput(cmd)
        err_string = 'Name or service not known'

        # If machine is up
        if (not err_string in output) and (scm_run_status == 'RUN' and ansible_run_status == 'NOTRUN'):
            if os.path.exists(new_err_log_file):
                with open(new_err_log_file, 'r') as f:
                    log_lines = f.readlines()
                for lline in log_lines:
                    if 'ERROR' in (lline.strip()):
                        # print(new_err_log_file)
                        print('%s,%s,%s' %
                              (hostname, ansible_run_status, lline.strip()))



if __name__ == '__main__':
    main()
