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
- https://www.thomas-krenn.com/de/wiki/Linux_ip_Kommando
- https://wiki.archlinux.org/title/dhcpcd
- https://wiki.ubuntuusers.de/NetworkManager/Dispatcher/
- https://askubuntu.com/questions/1024916/how-can-i-launch-a-systemd-service-at-startup-before-another-systemd-service-sta