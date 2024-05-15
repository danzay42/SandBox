1. install packages
2. config secure ssh
3. build & install python
4. config wsgi
5. config supervisor
6. config nginx

# Package
`gcc build-essential make vim htop git curl wget httpie unzip zip tmux mosh`

# sshd config
edit `/etc/ssh/sshd_config`
field:
  - AllowUser {logins}		# list of allowed users
  - PermitRootLogin no		# root not accepted
  - PasswordAuthentication no	# only ssh-keys

# install python from source
inside downloaded and extract folder with source
```shell
./configure --enable-optimization --prefix=$USER/.python/
make -j(nproc)
make install
# or
# make altinstall  # TODO check into source
```

# wsgi server
make config file inside project directory
  - gunicorn

# supervisor package
name: supervisor
sheme:
  nginx -> supervisor -> gunicorn/... -> gjango/flask/... project
