# PC-Bluray-Player-Tools Role

## 📌 Overview
Welcome to the `pc-bluray-player-tools` role, a part of the `cymais` repository. This role is dedicated to setting up software required for Blu-ray playback on personal computers. It focuses on installing necessary packages to enable the use of Blu-ray media with VLC player and other compatible software.

## Role Contents
The `main.yml` file in this role consists of tasks that automate the installation of the following packages:
1. **Install VLC and Blu-ray Software**:
   - `vlc`: A versatile media player that supports Blu-ray playback.
   - `libaacs`: A library for Blu-ray disc encryption handling.
   - `libbluray`: A library for Blu-ray disc playback support.

There are commented-out tasks for installing additional AUR packages, such as `aacskeys` and `libbdplus`, which can be enabled as per the user's requirements.

## 📚 Other Resources and Resources
For more in-depth information and guidance on Blu-ray playback and software configuration, the following resources can be consulted:
- [Arch Linux Wiki on Blu-ray](https://wiki.archlinux.org/title/Blu-ray#Using_aacskeys)
- [Guide to Play Blu-ray with VLC](https://videobyte.de/play-blu-ray-with-vlc)
- [Manjaro Forum Discussion on Blu-ray UHD Playback](https://archived.forum.manjaro.org/t/wie-kann-ich-bluray-uhd-abspielen/127396/12)
- [FV Online DB](http://fvonline-db.bplaced.net/)

## Dependencies
This role depends on the `java` role, which ensures the Java runtime is available – a requirement for certain Blu-ray playback tools and functionalities.

## Prerequisites
- **Ansible**: Ansible must be installed on your system to use this role.
- **Arch Linux-based System**: Designed for Arch Linux distributions, using the `pacman` package manager.

## Running the Role
To utilize this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-bluray-player-tools` directory.
3. Execute the role using Ansible, with appropriate permissions for installing packages.

## Customization
You can customize this role by enabling or adding additional tasks for other AUR packages related to Blu-ray playback as needed.

## Support and Contributions
For support, feedback, or contributions to enhance the role's capabilities, please open an issue or submit a pull request in the `cymais` repository. Contributions that improve Blu-ray playback support or compatibility are highly appreciated.