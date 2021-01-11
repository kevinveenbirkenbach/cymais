# Role Native Wireguard
Manages wireguard natively on host. More information are available in the [Arch wiki](https://wiki.archlinux.org/index.php/WireGuard#Manual_WireGuard_setup).

## Create Client Key
``bash
wg genkey | tee peer_A.key | wg pubkey > peer_A.pub
``

chown root:systemd-network /etc/systemd/network/99-*.netdev
chmod 0640 /etc/systemd/network/99-*.netdev
