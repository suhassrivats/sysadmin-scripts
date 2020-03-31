##################################################
# This script is related to Openstack project. It will find a matching
# aggregate for each flavor of OS in openstack
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2020}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Maintainer: {suhas srivats}
# Email: {contact_email}
# Status: {dev_status}
# Example: python3 flavor_aggregate_match.py
##################################################

import subprocess
import json


def write_to_file(output, command):
    file_name = command + '.json'
    with open(file_name, 'w') as f:
        f.write(output)


def json_to_dict(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def format_flavor_data(flavor_data):
    """Format flavor data to match aggregate data"""

    for i, ele in enumerate(flavor_data):
        flavor_prop_dict = {}
        flavor_prop = [i.split(':')[1]
                       for i in flavor_data[i]['Properties'].split(',')]

        # Delete properties (key-value pair) and append the formatted one
        del flavor_data[i]['Properties']

        for fp in flavor_prop:
            prop = fp.strip('"').split('=')
            flavor_prop_dict[prop[0]] = prop[1].strip("'")

        # Appending the formatted properties
        flavor_data[i]['Properties'] = flavor_prop_dict

    return flavor_data


def compare_two_dicts(flavor_dict_prop, aggregate_dict_prop):
    """
    For each flavor compare it with all aggregates and see if there is a match
    """

    # Initialize dictionaries for storing common properties
    flavor_dict_common = dict()
    aggregate_dict_common = dict()

    flavor_dict_set = set(flavor_dict_prop)
    aggregate_dict_set = set(aggregate_dict_prop)

    # Get the common properties of both dictionaries
    common_props = flavor_dict_set.intersection(aggregate_dict_set)

    # Make respective dictionaries with these common properties
    for prop in common_props:
        flavor_dict_common[prop] = flavor_dict_prop[prop]
        aggregate_dict_common[prop] = aggregate_dict_prop[prop]

    # Return True if equal, False otherwise
    return flavor_dict_common == aggregate_dict_common


def main():
    commands = ['flavor', 'aggregate']
    flav_aggr_map = dict()

    # Execute commands on a command line and write output to a JSON file
    for command in commands:
        cmd = ('/remote/kickstart/python-2.7.9/bin//openstack'
               ' %s list --long -f json' % (command))

        # Get output of a given command
        output = subprocess.getoutput(cmd)

        # Write output to a file in JSON format
        write_to_file(output, command)

    # Get flavor and aggregate JSON data in dictionary format
    flavor_data = format_flavor_data(json_to_dict('flavor.json'))
    aggregate_data = json_to_dict('aggregate.json')

    # Flavor to aggregates comparision
    for i, k1 in enumerate(flavor_data):
        for j, k2 in enumerate(aggregate_data):

            # Get flavor and aggregtate names
            flavor_name = flavor_data[i]['Name']
            aggregate_name = aggregate_data[j]['Name']

            # Compare properties of flavor with aggregate properties
            match = compare_two_dicts(
                flavor_data[i]['Properties'],
                aggregate_data[j]['Properties']
            )

            # If the properties are equal, then add flav-aggrs to a dictionary
            if match:
                if flavor_name not in flav_aggr_map:
                    flav_aggr_map[flavor_name] = [aggregate_name]
                else:
                    flav_aggr_map[flavor_name] += [aggregate_name]

    # Printing flavor-aggregate mappings
    for k,v in flav_aggr_map.items():
        print(k, ':', v)

    return flav_aggr_map


if __name__ == '__main__':
    main()
