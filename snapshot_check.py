##################################################
# Check snapshot of a NetApp cluster and alert if it is older than 10 days
##################################################
# Author: {Suhas Srivats Subburathinam}
# Copyright: Copyright {2018}, {Project: Check for older snapshots}
# Credits: [{credit_list}]
# License: {MIT}
# Version: {mayor}.{minor}.{rel}
# Mmaintainer: {suhas srivats}
# Email: {email_address}
# Status: {dev_status}
# Example: python snapshot_check.py
##################################################

import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

cmd = "/u/rwu/NTtool/sshpass-1.05/sshpass -p '<password>' ssh <cluster name> -l <username> -t 'snapshot show -vserver <vserver> -volume * -fields snapshot,create-time' > /tmp/out.txt"  # NOQA
os.system(cmd)

current_time = datetime.now()

alist = []


def email(html):

    # me == my email address
    # you == recipient's email address
    from_email = "from@exmaple.com"
    to_email = ["to1@example.com", "to2@example.com"]

    # Create message container - the correct MIME type is multipart/alternative
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Action Required! Snapshots older than 10 days in <cluster name>"
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)

    # Create the html of the message (a plain-text and an HTML version).
    # text = "Hi!\n\nPlease find all snapshots that are older than 7days"

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    # msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's
    # address and message to send - here it is sent as one string.
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()


def main():
    with open('/tmp/out.txt', 'r') as f:
        lines = f.readlines()

    # Remove unwanted entries from the list
    lines = lines[2:len(lines) - 2]

    html = ''
    html += "<html><body>"
    html += '<p>Hi,<br><br> Please take action as the snapshot usage may cause disk to be full. Please delete older snapshots mentioned below to avoid further issues.<br></p>'  # NOQA
    html += '<table border="1">'
    html += '<tr>'
    html += '<th> Cluster Name </th>'
    html += '<th> Volume Name </th>'
    html += '<th> Snapshot Name </th>'
    html += '<th> Snapshot Created at </th>'
    html += '</tr>'

    for line in lines:
        snapshot_policy = line.split()
        if len(snapshot_policy) == 8:
            snapshot_created_time = snapshot_policy[4] + ' ' + snapshot_policy[5] + \
                ' ' + snapshot_policy[7] + ' ' + snapshot_policy[6]
            snapshot_policy.append(snapshot_created_time)
            alist.append(snapshot_policy)

            diff = current_time - \
                datetime.strptime(snapshot_policy[8], '%b %d %Y %H:%M:%S')

            # snapshots older than 10 days
            if diff.days > 10:
                html += '<tr>'
                html += '<td> <cluster name> </td>'
                html += '<td> %s </td>' % snapshot_policy[1]
                html += '<td> %s </td>' % snapshot_policy[2]
                html += '<td> %s </td>' % snapshot_created_time
                html += '</tr>'

    html += '</table>'
    html += '<p>Regards,<br>Suhas</p>'
    html += '</body></html>'

    # Email HTML string
    email(html)


if __name__ == '__main__':
    main()
