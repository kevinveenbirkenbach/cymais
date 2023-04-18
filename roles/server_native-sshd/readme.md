# role server_native-sshd
## dependencies
This role depends on that a well configured user administrator exist.
For this reason this role depends on the role server_native-user-administrator.
A wrong configuration of this role can lead to an lockout of the system which just will be reversal via chroot.  

## PAM
- https://www.google.com/search?client=firefox-b-d&q=sshd+why+to+deactivate+pam

# see
- https://man7.org/linux/man-pages/man5/sshd_config.5.html
