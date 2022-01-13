#!/usr/bin/env python
# Compare previous and current public IP address, upload if necessary
# author: mellowizAThotmailDOTcom
# date (ISO 8601): 2018-01-05
# history:
#	1.3 fixed date, commented out 'remoteServer' 
#	1.2 moved the remote location to a global variable
#	1.1 replaced "curl" with "dig" pointing it to opendns.com
#	1.0 initial version

# Import some modules
from __future__ import print_function	# print() as a function not as a statement
import string				# common string operations
import subprocess			# spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import os				# portable way of using operating system dependent functionality

# Global settings
get_name = 'myip.opendns.com'
get_server = '@resolver1.opendns.com'
#remoteServer = 'user@example.org'

# Fetch the current literal public IP, PHP: getenv("REMOTE_ADDR")
# format: "x.y.w.z"
#currIP = string.strip(subprocess.check_output(['curl', '-s', get_my_publicIP]))
currIP = string.strip(subprocess.check_output(['dig', '+short', get_server, get_name]))

# Build the path to the previous IP address
thisHost = string.strip(subprocess.check_output(['hostname', '-s']))
thisHome = os.getenv('HOME')
prevIPfile = thisHome + '/' + thisHost + '_publicIP.log'

# Finally open file for appending
f = open(prevIPfile, 'a')

# Format: "x.y.w.z;<timestamp>"
last_ip_and_ts = currIP + ";" + str(subprocess.check_output('date'))

# Updates the local log file with the fetched public IP address
f.write(last_ip_and_ts)
f.close()

# Let's build the string that we'll use to update the remote log
remote_ip_and_ts = 'echo \"' + currIP + ';' + string.strip(str(subprocess.check_output('date'))) + '\" >> ~/WWW/files/raspi_publicIP'

# Append the latest info to the remote log
subprocess.Popen(['ssh', remoteServer, remote_ip_and_ts])
