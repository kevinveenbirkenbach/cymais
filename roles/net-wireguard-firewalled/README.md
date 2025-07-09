# WireGuard Client behind NAT

## Description

This role adapts iptables rules to enable proper connectivity for a WireGuard client running behind a NAT or firewall. It ensures that traffic is forwarded correctly by applying necessary masquerading rules.

## Overview

Optimized for environments with network address translation (NAT), this role:
- Executes shell commands to modify iptables rules.
- Allows traffic from the WireGuard client interface (e.g. `wg0-client`) and sets up NAT masquerading on the external interface (e.g. `eth0`).
- Works as an extension to the native WireGuard client role.

## Purpose

The primary purpose of this role is to enable proper routing and connectivity for a WireGuard client situated behind a firewall or NAT device. By adapting iptables rules, it ensures that the client can communicate effectively with external networks.

## Features

- **iptables Rule Adaptation:** Modifies iptables to allow forwarding and NAT masquerading for the WireGuard client.
- **NAT Support:** Configures the external interface for proper masquerading.
- **Role Integration:** Depends on the [net-wireguard-plain](../net-wireguard-plain/README.md) role to ensure that WireGuard is properly configured before applying firewall rules.

## Other Resources
- https://gist.github.com/insdavm/b1034635ab23b8839bf957aa406b5e39
- https://wiki.debian.org/iptables
