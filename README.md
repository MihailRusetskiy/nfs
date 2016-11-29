Requires python 2.7

In order to run tests, the user id in client hosts must
have access to run commands as root using the 'sudo' command without the need
for a password. This is used to run commands like 'mount' and 'umount'.
Furthermore, the user id must be able to ssh to remote hosts without the need
for a password.
for debugging purposes you can use --nomount flag


