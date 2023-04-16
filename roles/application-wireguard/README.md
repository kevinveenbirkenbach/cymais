# Role Native Wireguard
Manages wireguard on a client.

## Create Client Keys
```bash
  wg_private_key="$(wg genkey)"
  wg_public_key="$(echo "$wg_private_key" | wg pubkey)"
  echo "PrivateKey: $wg_private_key"
  echo "PublicKey: $wg_public_key"
  echo "PresharedKey: $(wg genpsk)"
```

## Debug 

### RTNETLINK answers: Permission denied
When ```systemctl restart wg-quick@wg0.service``` returns __RTNETLINK answers: Permission denied__, modify _/etc/sysctl.conf_:

```bash
net.ipv6.conf.all.disable_ipv6 = 0
net.ipv6.conf.default.disable_ipv6 = 0
net.ipv6.conf.lo.disable_ipv6 = 0
```

Afterwards reload: 
```bash
sysctl -p
systemctl restart wg-quick@wg0.service
```


### SSH

When the SSH connection over wireguard is buggy try: 

```bash
ip li set mtu 1400 dev eth0
ip li set mtu 1400 dev wlo1
```

This can be connected to the [MTU](https://www.imperva.com/learn/application-security/what-is-mtu-mss/)

## Other
- https://golb.hplar.ch/2019/01/expose-server-vpn.html
- https://wiki.archlinux.org/index.php/WireGuard
- https://wireguard.how/server/raspbian/
- https://www.scaleuptech.com/de/blog/was-ist-und-wie-funktioniert-subnetting/
- https://bodhilinux.boards.net/thread/450/wireguard-rtnetlink-answers-permission-denied
- https://stackoverflow.com/questions/69140072/unable-to-ssh-into-wireguard-ip-until-i-ping-another-server-from-inside-the-serv
- https://unix.stackexchange.com/questions/717172/why-is-ufw-blocking-acces-to-ssh-via-wireguard
- https://forum.openwrt.org/t/cannot-ssh-to-clients-on-lan-when-accessing-router-via-wireguard-client/132709/3
- https://serverfault.com/questions/1086297/wireguard-connection-dies-on-ubuntu-peer
- https://unix.stackexchange.com/questions/624987/ssh-fails-to-start-when-listenaddress-is-set-to-wireguard-vpn-ip
- https://serverfault.com/questions/210408/cannot-ssh-debug1-expecting-ssh2-msg-kex-dh-gex-reply