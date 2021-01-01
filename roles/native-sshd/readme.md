# role native-sshd
## dependencies
This role depends on that a well configured user administrator exist.
For this reason this role depends on the role native-user-administrator.
A wrong configuration of this role can lead to an lockout of the system which just will be reversal via chroot.  

## PAM
- https://www.google.com/search?client=firefox-b-d&q=sshd+why+to+deactivate+pam
