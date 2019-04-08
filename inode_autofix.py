##################################################
# This script will check within a NetApp storage cluster, if an indoe
# used-files is greater than a threshold value, then it will auto-grow total
# inodes in a volume - NetApp
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Maintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 inode_autofix.py
# Shebang: #!/depot/python/bin/python
##################################################

import sys
import os
import subprocess
import logging
import datetime

# Define threshold values
max_files_count = 2000000000
constituent_vol_files_used_percent_threshold = 80
number_of_constituents = 24


# Create a logging file and update it
logging.basicConfig(filename='logmodule_inode_autofix.log',level=logging.DEBUG)

# Get current datetime
currentDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

clusters = ['cluster1', 'cluster2']
for cluster in clusters:
    logging.info("#" * 50)
    logging.info("%s:%s" % (currentDT, cluster.upper()))
    # print("#" * 50)
    # print("%s:%s" % (currentDT, cluster.upper()))

    # Get inode information for all volumes in a cluster
    cmd = "ssh %s 'vol show * -fields files, files-used -vserver %svs1'" % (cluster, cluster)
    output = subprocess.getoutput(cmd).strip('\n').split('\n')

    for vol in output[4:-1]:
        # Parse and get all relavent information
        vserver = vol.split()[0]
        vol_name = str(vol.split()[1])

        if not (vol.split()[2]) == '-':
            vol_total_files = int(vol.split()[2])
            vol_files_used = int(vol.split()[3].strip('%'))

        # Check if max inode count is reached. If yes, no action should be taken
        if vol_total_files >= max_files_count:
            logging.warning("Max inode count reached. Cannot increase anymore for volume: %s" % vol_name)
            # print("Max inode count reached. Cannot increase anymore for volume: %s" % vol_name)

        # Check for volumes' consitituents used-inodes
        else:
            cmd = "ssh %s 'vol show %s* -is-constituent true -fields files, files-used -vserver %svs1'" % (cluster, vol_name , cluster)
            output = subprocess.getoutput(cmd).strip('\n').split('\n')

            for constituent_vol in output[4:-1]:
                vserver = constituent_vol.split()[0]
                constituent_vol_name = str(constituent_vol.split()[1])
                constituent_vol_total_files = int(constituent_vol.split()[2])
                constituent_vol_files_used = int(constituent_vol.split()[3].strip('%'))
                constituent_vol_files_used_percent = (constituent_vol_files_used/constituent_vol_total_files) * 100

                # If constituent's used-inodes is greater than threshold, then update the top-level
                if constituent_vol_files_used_percent > constituent_vol_files_used_percent_threshold:
                    new_vol_total_files = (constituent_vol_total_files * 1.15 * number_of_constituents)

                    if not (new_vol_total_files > (0.85 * max_files_count)):
                        vol_inode_increase = ("ssh %s volume modify -volume %s -files %s -vserver %svs1" % (cluster, vol_name, round(new_vol_total_files), cluster))
                        logging.info("%s:%s === %s" % (currentDT, vol_inode_increase, constituent_vol_name))
                        # print("%s:%s === %s" % (currentDT, vol_inode_increase, constituent_vol_name))
                        vol_inode_increase_output = subprocess.getoutput(vol_inode_increase)
                        logging.debug(vol_inode_increase_output)
                        # print(vol_inode_increase_output)
                        break

                    if (new_vol_total_files > (0.85 * max_files_count)):
                        logging.info("%s:New total-files count for %s in %s is greater than 85 percent of max_files_count. Cannot increase inode." % (currentDT, constituent_vol_name, cluster))
                        # print("%s:New total-files count for %s in %s is greater than 85 percent of max_files_count. Cannot increase inode." % (currentDT, constituent_vol_name, cluster))
                        break

    logging.info("#" * 50)
    # print("#" * 50)
