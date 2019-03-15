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
# Mmaintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 inode_autofix.py
##################################################

import sys
import os
import subprocess

#Define thresholds here
max_files_count = 2000000000
constituent_vol_files_used_percent_threshold = 80
number_of_constituents = 24

clusters = ['cluster1', 'cluster2']
for cluster in clusters:
    print("#" * 50)
    print(cluster.upper())
    # Get inode information for all volumes in a cluster
    cmd = "ssh %s 'vol show * -fields files, files-used -vserver %svs1'" % (cluster, cluster)
    output = subprocess.getoutput(cmd).strip('\n').split('\n')
    # print(output)

    for vol in output[4:-1]:
        # print(vol)
        # Parse and get all relavent information
        vserver = vol.split()[0]
        vol_name = str(vol.split()[1])
        vol_total_files = int(vol.split()[2])
        vol_files_used = int(vol.split()[3].strip('%'))

        # Check if max inode count is reached. If yes, no action should be taken
        if vol_total_files >= max_files_count:
            print("Max inode count reached. Cannot increase anymore!", vol_name)

        # Check for volumes' consitituents used inodes.
        else:
            cmd = "ssh %s 'vol show %s* -is-constituent true -fields files, files-used -vserver %svs1'" % (cluster, vol_name , cluster)
            output = subprocess.getoutput(cmd).strip('\n').split('\n')

            for constituent_vol in output[4:-1]:
                vserver = constituent_vol.split()[0]
                constituent_vol_name = str(constituent_vol.split()[1])
                constituent_vol_total_files = int(constituent_vol.split()[2])
                constituent_vol_files_used = int(constituent_vol.split()[3].strip('%'))
                constituent_vol_files_used_percent = (constituent_vol_files_used/constituent_vol_total_files) * 100

                # If constituent used inodes is greater than threshold, then update the top-level
                if constituent_vol_files_used_percent > constituent_vol_files_used_percent_threshold:
                    # print('Files used for this constituent volume is greater than threshold value: ', constituent_vol_name)
                    new_vol_total_files = (constituent_vol_total_files * 1.15 * number_of_constituents)
                    if not (new_vol_total_files > (0.85 * max_files_count)):
                        print("ssh %s volume modify -volume %s -files %s -vserver %svs1" % (cluster, vol_name, round(new_vol_total_files), cluster), '===', constituent_vol_name)
                        # os.system(vol_inode_increase)
                        break
                    if (new_vol_total_files > (0.85 * max_files_count)):
                        print("New total volume count is greater than 85 percent of max_files_count. Cannot increase inode")

    print("#" * 50)
