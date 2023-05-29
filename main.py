import json, subprocess, time

# Global settings
thisHostname = subprocess.check_output(['hostname']).rstrip().decode('utf-8')
resolverURL = 'https://myipv4.p1.opendns.com/get_my_ip'
remoteServer = '<user>@<remote_server>'                      # replace with your own account
waitTime = 3600                                              # default interval, 3600s = 1h
privateKey = '/root/.ssh/private.my'                         # place your own private key inside the target file
knownHosts = '/root/.ssh/known_hosts.my'                     # dummy file, placeholder

# Main function, infinite loop
while True:
    # Fetch the current literal public IP, PHP: getenv("REMOTE_ADDR")
    # format: "x.y.w.z"
#    currIP = subprocess.check_output(['dig', '+short', get_server, get_name]).rstrip().decode('utf-8')
    currIP4 = subprocess.check_output(['curl', '-s', resolverURL])
    currIP4_json = json.loads(currIP4)
    currIP = currIP4_json['ip']

    # Let's build the string that we'll use to update the remote log
    outData = currIP + ';' + subprocess.check_output('date').rstrip().decode('utf-8') + ';' + thisHostname
    remote_ip_ts_hn = 'echo \"' + outData + '\" >> ~/SWWW/raspi_publicIP'

    # Append the latest info to the remote log, SSH will be 'password-less' if public key has been added to remoteServer's authorized_keys
    subprocess.Popen(['ssh', '-i', privateKey, '-o', 'UserKnownHostsFile=' + knownHosts , remoteServer, remote_ip_ts_hn])
    print(outData)
    time.sleep(waitTime)

