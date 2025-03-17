# Java

## Overview
This README file is for the Java role, which is part of the `cymais`. The role is specifically designed to automate the installation of Java on a system, focusing on the OpenJDK 11 version.

## Contents of the role
The `main.yml` file within the `java` role consists of a single, but crucial task:

1. **Install Java**: This task uses the `community.general.pacman` module to install the `jdk11-openjdk` package. It ensures that Java Development Kit 11 (OpenJDK 11) is present on the system.

## Purpose
The primary objective of this role is to provide a straightforward and efficient method for setting up Java, specifically JDK 11, on personal computers or development environments. This setup is essential for developers who work with Java or run applications that require the Java runtime environment.

## Prerequisites
- **Ansible**: You need to have Ansible installed on your system to use this role.
- **Arch Linux-based System**: The role uses the `pacman` package manager, indicating that it is intended for use on systems based on Arch Linux or its derivatives.

## Running the role
To run this role:
1. Clone the `computer-role` repository to your system.
2. Navigate to the `roles/java` directory within the repository.
3. Execute the role using Ansible. Make sure you have the necessary permissions to install packages on your system.

## Customization
This role is focused on installing JDK 11, but it can be easily modified to install different versions of the JDK or additional Java-related tools as per your requirements.

## Support and Contribution
For support, feedback, or contributions to the role, please open an issue or submit a pull request in the `cymais` repository. Contributions that enhance the role or broaden its applicability are greatly appreciated.