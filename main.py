import subprocess, time

# Global settings
thisHostname = subprocess.check_output(['hostname']).rstrip().decode('utf-8')
get_name = 'myip.opendns.com'
get_server = '@resolver1.opendns.com'
remoteServer = '<user>@<remote_server>'
waitTime = 300
privateKey = '/root/.ssh/private.my'         # replace with your own private key
knownHosts = '/root/.ssh/known_hosts.my'     # dummy file, placeholder

# Main function, infinite loop
while True:
    # Fetch the current literal public IP, PHP: getenv("REMOTE_ADDR")
    # format: "x.y.w.z"
    currIP = subprocess.check_output(['dig', '+short', get_server, get_name]).rstrip().decode('utf-8')

    # Let's build the string that we'll use to update the remote log
    outData = currIP + ';' + subprocess.check_output('date').rstrip().decode('utf-8') + ';' + thisHostname
#    remote_ip_ts_hn = 'echo \"' + outData + '\" >> ~/WWW/files/raspi_publicIP'
    remote_ip_ts_hn = 'echo \"' + outData + '\" >> ~/SWWW/raspi_publicIP'

    # Append the latest info to the remote log, SSH will be 'password-less' if public key has been added to remoteServer's authorized_keys
    subprocess.Popen(['ssh', '-i', privateKey, '-o', 'UserKnownHostsFile=' + knownHosts , remoteServer, remote_ip_ts_hn])
    print(outData)
    time.sleep(waitTime)

