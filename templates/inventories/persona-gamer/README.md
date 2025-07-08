# Gamer 🎮

## Description

This Ansible meta-role prepares an Arch Linux system for a complete and optimized gaming experience. It delegates the setup to modular sub-roles that install open-source games, retro emulators, and core performance tools like [Steam](https://store.steampowered.com/), [Wine](https://www.winehq.org/), [Lutris](https://lutris.net/), [GameMode](https://github.com/FeralInteractive/gamemode), and [RetroArch](https://www.retroarch.com/).

## Overview

This role combines several specialized gaming roles into one streamlined setup. It ensures your system is ready for modern, retro, and open-source gaming, with zero manual configuration.

## Purpose

To provide a modular and reproducible way to deploy a full-featured Linux gaming system, suited for both native and Windows-based titles, retro consoles, and FOSS games.

## Features

- ✅ **Modular Roles:** Handles separate responsibilities through sub-roles
- 🕹️ **Retro Support:** Emulators and themes via [RetroArch](https://www.retroarch.com/)
- 🧩 **Core Stack:** Performance tools and runtimes (e.g. [GameMode](https://github.com/FeralInteractive/gamemode), [MangoHUD](https://github.com/flightlessmango/MangoHud))
- 🎲 **Open Source Games:** Installed directly from official Arch repos
- ⚙️ **System Integration:** Sets `gaming_ready` fact for other CyMaIS roles

## Sub-Roles

| Role | Responsibility |
|------|----------------|
| [`persona-gamer-retro`](../persona-gamer-retro) | Installs RetroArch and assets |
| [`persona-gamer-default`](../persona-gamer-default) | Installs open source games |
| [`persona-gamer-core`](../persona-gamer-core) | Installs Steam, Lutris, Wine, GameMode, MangoHUD |

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**  
Learn more at [www.veen.world](https://www.veen.world)

Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)