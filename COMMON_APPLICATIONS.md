### Base Setup

Provides essential configurations for system initialization, including hostname setting, systemd journal management, locale configurations, and swapfile handling.

- **[Hostname](./roles/hostname/)**: Sets the system's hostname.
- **[Journalctl](./roles/journalctl/)**: Configures systemd journal settings.
- **[Locales](./roles/locales/)**: Configures system locales.
- **[System-Swapfile](./roles/system-swapfile/)**: Configures swapfile creation and management.

### Administration Tools

Includes necessary tools for effective system administration, such as Git setup, Linux admin tools, and sudo configuration.

- **[Git](./roles/git/)**: Basic Git version control system setup.
- **[PC-Administrator-Tools](./roles/pc-administrator-tools/)**: Installs basic Linux administration tools.
- **[Sudo](./roles/sudo/)**: Installs and configures sudo.

### Update
Covers automated updates and maintenance for the system and its components, including package managers and Docker containers.
- **[update](./roles/update/)**: Automates the process of system updates.
- **[update-apt](./roles/update-apt/)**: Updates system packages using apt (for Debian-based systems).
- **[update-docker](./roles/update-docker/)**: Keeps Docker containers up to date.
- **[update-pacman](./roles/update-pacman/)**: Updates system packages using Pacman (for Arch-based systems).
- **[update-yay](./roles/update-yay/)**: Updates system packages using yay.

### Driver
Deals with the installation and configuration of various hardware drivers, catering to a range of devices and needs.
- **[driver-epson-multiprinter](./roles/driver-epson-multiprinter/)**: Installs drivers for Epson multi-function printers.
- **[driver-intel](./roles/driver-intel/)**: Installs Intel drivers, typically for graphics and other hardware.
- **[driver-msi-keyboard-color](./roles/driver-msi-keyboard-color/)**: Configures MSI keyboard color settings.
- **[driver-non-free](./roles/driver-non-free/)**: Installs non-free drivers, generally for specific hardware needs.

### Security
Enhances system security through roles focused on security measures, swap file management, user configurations, and SSH settings.
- **[System Security](./roles/system-security/)**: Enhances overall system security.
- **[System Swapfile](./roles/system-swapfile/)**: Manages swap files for system memory.
- **[User Administrator](./roles/user-administrator/)**: Setup for system administrator user.
- **[User Alarm](./roles/user-alarm/)**: Manages the alarm user.
- **[PC SSH](./roles/pc-ssh/)**: Configuration of SSH for secure remote access.
- **[SSHD](./roles/sshd/)**: Configures SSH daemon settings.

### Virtual Private Network (VPN)
Centers on VPN configurations, specifically for Wireguard, providing secure and efficient network connectivity.
- **[client-wireguard](./roles/client-wireguard/)**: Configures Wireguard VPN client.
- **[client-wireguard-behind-firewall](./roles/client-wireguard-behind-firewall/)**: Sets up Wireguard client functionality behind a firewall.
- **[wireguard](./roles/wireguard/)**: Installs and configures Wireguard for secure VPN connections.

#### Notifier
Introduces roles for setting up system event notifications, with options for email and Telegram alerts.
- **[Systemd-Notifier](./roles/systemd-notifier/)**: Notifier service for systemd.
- **[Systemd-Notifier-Email](./roles/systemd-notifier-email/)**: Email notifications for systemd services.
- **[Systemd-Notifier-Telegram](./roles/systemd-notifier-telegram/)**: Telegram notifications for systemd services.

### Backup Solutions
Focuses on comprehensive backup strategies and cleanup procedures, encompassing data backups, remote server backups, and maintenance of backup storage efficiency.

#### Backups
- **[backup-data-to-usb](./roles/backup-data-to-usb/)**: Automates data backup to USB devices.
- **[backup-docker-to-local](./roles/backup-docker-to-local/)**: Backs up Docker volumes to local storage.
- **[backup-remote-to-local](./roles/backup-remote-to-local/)**: Pulls backups from remote servers for local storage.
- **[backups-provider](./roles/backups-provider/)**: Manages backup processes and storage solutions.
- **[backups-provider-user](./roles/backups-provider-user/)**: Creates and configures users for backup processes.

#### Backups Cleanup
- **[cleanup-backups-service](./roles/cleanup-backups-service/)**: Service to clean up old backups automatically.
- **[cleanup-backups-timer](./roles/cleanup-backups-timer/)**: Timer for scheduling the backup cleanup service.
- **[cleanup-disc-space](./roles/cleanup-disc-space/)**: Manages and frees up disk space on the system.
- **[cleanup-failed-docker-backups](./roles/cleanup-failed-docker-backups/)**: Cleans up failed Docker backups.

### Other
Encompasses miscellaneous essential tools and systems, including AUR helper, spellchecking, typesetting, and package management.
- **[System-Aur-Helper](./roles/system-aur-helper/)**: Installs and configures AUR helper (yay).
- **[Hunspell](./roles/hunspell/)**: Installation of Hunspell spellchecker.
- **[Latex](./roles/pc-latex/)**: Installation of LaTeX typesetting system.
- **[Java](./roles/java/)**: Installs Java Development Kit (JDK).
- **[Python Pip](./roles/python-pip/)**: Installation of Python Pip package manager.
