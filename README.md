# Client Playbook
Playbook to setup Manjaro GNOME clients.
# Setup

Run:
```bash
ansible-galaxy collection install -r requirements.yml
```

# Todo
- add ssh
# Refactor
```bash
FSTAB_SWAP_ENTRY="/swapfile none swap defaults 0 0"
SWAP_FILE="/swapfile"
FSTAB_FILE="/etc/fstab"
if grep -q "$FSTAB_SWAP_ENTRY" "$FSTAB_FILE"; then
	info "Skipping creation of swap partion because entry allready exists in \"$FSTAB_FILE\"!"
else
	info "Creating swap partition..." &&
	sudo fallocate -l 16G "$SWAP_FILE" &&
	sudo chmod 600 "$SWAP_FILE" &&
	sudo mkswap "$SWAP_FILE" &&
	sudo swapon "$SWAP_FILE" &&
	sudo sh -c "echo \"$FSTAB_SWAP_ENTRY\">>\"$FSTAB_FILE\"" || error "Creation of swap partition failed."
fi

info "Setup SSH key..."
ssh_key_path="$HOME/.ssh/id_rsa"
if [ ! -f "$ssh_key_path" ]; then
	info "SSH key $ssh_key_path doesn't exists!"
	if [ ! -f "./data$ssh_key_path" ]; then
		info "Importing ssh key by copying data..." &&
		bash "$SCRIPT_PATH""/data/export-to-system.sh" || error "Copying failed."
	else
		info "Generating ssh key..." &&
		ssh-keygen -t rsa -b 4096 -C "$USER@$HOSTNAME" || error "Key generation failed."
	fi
fi

info "Setup, configuration and installation of dependencies for installed software..."

if pacman -Qi "arduino" > /dev/null ; then
	info "Configurate system for arduino..." &&
	sudo usermod -a -G uucp "$USER" &&
	sudo usermod -a -G lock "$USER" || error "Couldn't add \"$USER\" to the relevant groups."
fi

if pacman -Qi "docker" > /dev/null ; then
	info "Setting up docker..." &&
	info "Add current user \"$USER\" to user group docker..." &&
	sudo usermod -a -G docker "$USER" || error "Failed to add user."
	info "Restarting docker service..." &&
	sudo systemctl restart docker &&
	info "Disable and stop docker service..." &&
	sudo systemctl disable --now docker || error "\"systemctl\" produced an error."
	info "For performance reasons docker is not enabled. Start docker by executing \"sudo systemctl restart docker\" when you need it."
fi

if [ ! "$(pacman -Qi "virtualbox")" ] ; then
	info "Setting up virtualbox..." &&
	sudo pacman -S virtualbox "$(pacman -Qsq "^linux" | grep "^linux[0-9]*[-rt]*$" | awk '{print $1"-virtualbox-host-modules"}' ORS=' ')" &&
	sudo vboxreload &&
	pamac build virtualbox-ext-oracle &&
	sudo gpasswd -a "$USER" vboxusers || error
	info "Keep in mind to install the guest additions in the virtualized system. See https://wiki.manjaro.org/index.php?title=VirtualBox"
fi

install_gnome_extension(){
	info "Install GNOME extension \"$1\"..."
	extension_folder="$HOME/.local/share/gnome-shell/extensions/$1/"
	if [ -d "$extension_folder" ];
		then
			if [ -d "$extension_folder"".git" ];
				then
					warning "Found a .git repository didn't expect to find this here." &&
					info "Pulling changes from git..." &&
					(cd "$extension_folder" && git pull) || error
			else
				info "No git repository. Extension will not be updated."
			fi
		else
			info "Install..." &&
			git clone "$2" "$extension_folder" || error
	fi

	if [ -f "$extension_folder""Makefile" ];
		then

			tmp_extension_folder="/tmp/$1"
			mv "$extension_folder" "$tmp_extension_folder"
			info "Compilling extension.."
			(cd "$tmp_extension_folder" && make install) || error "Compilation with failed."

			info "Cleaning up tmp-extension folder..."&&
			rm -fr "$tmp_extension_folder" || error

		else
			info "No Makefile found. Skipping compilation..."
	fi

	info "Activating GNOME extension \"$1\"..." &&
	gnome-extensions enable "$1" || error
}

if [ "$DESKTOP_SESSION" == "gnome" ]; then
  info "Synchronizing gnome tools..." &&
  install_yay_packages_if_needed "$(get_packages "client/yay/gnome")" || error "Syncronisation failed."
	info "Install GNOME extensions..." &&
	install_gnome_extension "nasa_apod@elinvention.ovh" "https://github.com/Elinvention/gnome-shell-extension-nasa-apod.git"
  install_gnome_extension "caffeine@patapon.info" "https://github.com/eonpatapon/gnome-shell-extension-caffeine.git"
	info "Deactivating \"Dash to Dock\"..." &&
	gnome-extensions disable dash-to-dock@micxgx.gmail.com || error

fi
```

# See
- https://www.middlewareinventory.com/blog/run-ansible-playbook-locally/
- https://stackoverflow.com/questions/30533372/run-an-ansible-task-only-when-the-hostname-contains-a-string
