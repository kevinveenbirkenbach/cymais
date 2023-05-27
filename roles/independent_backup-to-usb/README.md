# independent_backup-to-usb

This Ansible role automates the process of performing backups to a swappable USB device.

## Features

- Automatically starts the backup process when a specific USB device is plugged in.
- Provides a systemd service to run the backup script at boot if the USB device is already connected.
- Supports customization of the backup source path and mount point.

## Configuration

The following variables can be customized in the `vars/main.yml` file:

- `mount_point`: The mount point where the USB device will be mounted.
- `backup_to_usb_script_path`: The path to the backup script that will be executed when the USB device is connected.

## Credits

This role was created and maintained by Kevin Veen-Birkenbach.
Contact: kevin@veen.world

## More Information

For more details on how the `independent_backup-to-usb` role works, please refer to the Ansible documentation and the role's source code.