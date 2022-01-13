# DynGo2Home
Provides a method to advertise the public IP address so that connecting back home is possible.</br>
In a similar fashion to some well-known services, this application dynamically updates the value of the public IP as seen from behind your home router.</br>
<br/>
## Notes
This application requires SSH access to some server accessible in the public Internet.<br/>
To achieve this without the need to enter username/password, PKI must be setup between the two nodes as follows.</br>
- Local node
  - copy/edit both `Dockerfile` and `main.py` (see [Diffs](#diffs) section at the bottom), e.g.: `Dockerfile.my` `mainpy.my`
  - create or copy public+private keypair (e.g. `ssh-keygen -t rsa -f private`): `private.my` `private.pub.my`
  - create or copy one file containing the remote server's key: `ssh-keygen -F <remote_server> > known_hosts.my`
  - TEST: `ssh -i private.my <user>@<remote_server> "uname -a"`

<b>NOTE</b>: all of the files above have been given `.my` extension to match the corresponding rule in `.gitignore` to avoid pushing any customized files to the remote repo!

- Remote node
  - store the public key into `.ssh/authorized_keys`
  - <b>Do not forget</b> to run `chmod 600 <your-private-and-public-keys>`!

## Build, push, quick run...
```
docker build -t <repository>/<image>:<tag> -f Dockerfile.my .

docker push <repository>/<image>:<tag>

docker run \
    --detach \
    [--rm] \
    [--restart=always] \
    --volume /absolute_path_to/private-and-public-keys:/root/.ssh:ro \
    <repository>/<image>:<tag>
```

<b>Options</b> (mutually exclusive):</br>
`--rm`: Automatically remove the container when it exits<br/>
`--restart=always`: Restart policy to apply when a container exits</br>

## <a name="diffs"></a>Diffs
Default Dockerfile vs. Dockerfile.my
```
$ diff Dockerfile Dockerfile.my
5c5
< COPY main.py ${DESTDIR}
---
> COPY mainpy.my ${DESTDIR}
```
Default main.py vs. mainpy.my
```
$ diff main.py mainpy.my
7c7
< remoteServer = '<user>@<remote_server>'
---
> remoteServer = 'user@example.org'
```

## Deploy to Swarm
Prepare the nodes
```
for idx in {1..4}
    do ssh pi@p${idx}.local "mkdir -p github/DynGo2Home"
done

for idx in {1..4}
    do scp private.my known_hosts.my pi@p${idx}.local:github/DynGo2Home 
done
```

Create service, run it
```
pi@ctrl $ docker service create --name dyngo2home carmelo0x99/dyngo2home:2.1
0pckeiv4glhspkyg88pnuf0ii
overall progress: 1 out of 1 tasks
1/1: running   [==================================================>]
verify: Service converged

pi@ctrl $ docker service ls
ID                  NAME             MODE                REPLICAS     IMAGE                        PORTS
0pckeiv4glhs        dyngo2home       replicated          1/1          carmelo0x99/dyngo2home:2.1

pi@ctrl $ docker service ps dyngo2home
ID                  NAME             IMAGE                     NODE   DESIRED STATE    CURRENT STATE            ERROR     PORTS
z0e3yep0e60m        dyngo2home.1     carmelo0x99/dyngo2home:2.1   ctrl   Running          Running 19 seconds ago

pi@ctrl $ docker service scale dyngo2home=2
dyngo2home scaled to 2
overall progress: 2 out of 2 tasks
1/2: running   [==================================================>]
2/2: running   [==================================================>]
verify: Service converged

pi@ctrl $ docker service ls
ID                  NAME             MODE                REPLICAS     IMAGE                        PORTS
0pckeiv4glhs        dyngo2home       replicated          2/2          carmelo0x99/dyngo2home:2.1

pi@ctrl $ docker service ps dyngo2home
ID                  NAME             IMAGE                        NODE   DESIRED STATE    CURRENT STATE            ERROR     PORTS
z0e3yep0e60m        dyngo2home.1     carmelo0x99/dyngo2home:2.1   ctrl   Running          Running 3 minutes ago
9ggd9pz1ux7m        dyngo2home.2     carmelo0x99/dyngo2home:2.1   p3     Running          Running 11 seconds ago
```

