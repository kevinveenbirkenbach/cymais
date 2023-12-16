# Common Applications
This section outlines the common applications tailored for both servers and end-users, offering a wide range of functionalities to enhance system performance, security, and usability.

## Base Setup
Key for initial system configuration, this section includes hostname setting, systemd journal management, locale configurations, and swapfile handling. Essential for both server and end-user setups, it ensures a solid foundation for system operations.

- **[Hostname](./roles/hostname/)**: Sets the system's hostname.
- **[Journalctl](./roles/journalctl/)**: Configures systemd journal settings.
- **[Locales](./roles/locales/)**: Configures system locales.
- **[System-Swapfile](./roles/system-swapfile/)**: Configures swapfile creation and management.

## Administration Tools
These tools are crucial for effective system administration, encompassing Git setup, Linux admin tools, and sudo configuration, suitable for both server environments and power users.

- **[Git](./roles/git/)**: Basic Git version control system setup.
- **[Administrator-Tools](./roles/pc-administrator-tools/)**: Installs basic Linux administration tools.
- **[Sudo](./roles/sudo/)**: Installs and configures sudo.

## Update
This category focuses on automated updates and maintenance for the system and its components, including package managers and Docker containers, ensuring systems are up-to-date and secure.

- **[update](./roles/update/)**: Automates the process of system updates.
- **[update-apt](./roles/update-apt/)**: Updates system packages using apt (for Debian-based systems).
- **[update-docker](./roles/update-docker/)**: Keeps Docker containers up to date.
- **[update-pacman](./roles/update-pacman/)**: Updates system packages using Pacman (for Arch-based systems).
- **[update-yay](./roles/update-yay/)**: Updates system packages using yay.

## Driver
Caters to a range of devices and needs for hardware driver installation and configuration, an integral part for both server hardware optimization and end-user device functionality.

- **[driver-epson-multiprinter](./roles/driver-epson-multiprinter/)**: Installs drivers for Epson multi-function printers.
- **[driver-intel](./roles/driver-intel/)**: Installs Intel drivers, typically for graphics and other hardware.
- **[driver-msi-keyboard-color](./roles/driver-msi-keyboard-color/)**: Configures MSI keyboard color settings.
- **[driver-non-free](./roles/driver-non-free/)**: Installs non-free drivers, generally for specific hardware needs.

## Security
Enhances system security with roles focused on security measures, user configurations, and SSH settings. It's vital for protecting both server environments and end-user systems.
- **[System Security](./roles/system-security/)**: Enhances overall system security.
- **[User Administrator](./roles/user-administrator/)**: Setup for system administrator user.
- **[User Alarm](./roles/user-alarm/)**: Manages the alarm user.
- **[PC SSH](./roles/pc-ssh/)**: Configuration of SSH for secure remote access.
- **[SSHD](./roles/sshd/)**: Configures SSH daemon settings.
- **[System Maintanance Lock](./roles/system-maintenance-lock)**: Locks maintenance services to prevent dangerous inteactions between services

## Virtual Private Network (VPN)
Centers on VPN configurations for secure and efficient network connectivity, particularly crucial for remote server access and end-users needing secure connections.
- **[client-wireguard](./roles/client-wireguard/)**: Configures Wireguard VPN client.
- **[client-wireguard-behind-firewall](./roles/client-wireguard-behind-firewall/)**: Sets up Wireguard client functionality behind a firewall.
- **[wireguard](./roles/wireguard/)**: Installs and configures Wireguard for secure VPN connections.

## Notifier
Sets up system event notifications via email and Telegram, a versatile feature for server administrators and end-users alike to stay informed about their system's status.
- **[Systemd-Notifier](./roles/systemd-notifier/)**: Notifier service for systemd.
- **[Systemd-Notifier-Email](./roles/systemd-notifier-email/)**: Email notifications for systemd services.
- **[Systemd-Notifier-Telegram](./roles/systemd-notifier-telegram/)**: Telegram notifications for systemd services.

## Backup Solutions
Focuses on comprehensive backup strategies and cleanup procedures, encompassing data backups, remote server backups, and maintenance of backup storage efficiency, crucial for data integrity in both servers and personal devices.

### Backups
For USB devices, Docker volumes, remote servers, and user configurations.
- **[backup-data-to-usb](./roles/backup-data-to-usb/)**: Automates data backup to USB devices.
- **[backup-docker-to-local](./roles/backup-docker-to-local/)**: Backs up Docker volumes to local storage.
- **[backup-remote-to-local](./roles/backup-remote-to-local/)**: Pulls backups from remote servers for local storage.
- **[backups-provider](./roles/backups-provider/)**: Manages backup processes and storage solutions.
- **[backups-provider-user](./roles/backups-provider-user/)**: Creates and configures users for backup processes.

### Backups Cleanup
Manages disk space and cleans up old or failed backups.
- **[cleanup-backups-service](./roles/cleanup-backups-service/)**: Service to clean up old backups automatically.
- **[cleanup-backups-timer](./roles/cleanup-backups-timer/)**: Timer for scheduling the backup cleanup service.
- **[cleanup-disc-space](./roles/cleanup-disc-space/)**: Manages and frees up disk space on the system.
- **[cleanup-failed-docker-backups](./roles/cleanup-failed-docker-backups/)**: Cleans up failed Docker backups.

## Other
Encompasses miscellaneous essential tools and systems, including package management, spellchecking, and typesetting, beneficial for both server maintenance and enhancing end-user experience.
- **[System-Aur-Helper](./roles/system-aur-helper/)**: Installs and configures AUR helper (yay).
- **[Hunspell](./roles/hunspell/)**: Installation of Hunspell spellchecker.
- **[Latex](./roles/pc-latex/)**: Installation of LaTeX typesetting system.
- **[Java](./roles/java/)**: Installs Java Development Kit (JDK).
- **[Python Pip](./roles/python-pip/)**: Installation of Python Pip package manager.
