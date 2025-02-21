# Mailu Server Docker Role 🚀

This guide provides instructions for setting up, operating, and maintaining the [Mailu](https://mailu.io/) server Docker role.

## Table of Contents 📖

- [Setup](#setup)
  - [Fetchmail Issues](#fetchmail-issues)
  - [Data Deletion](#data-deletion)
  - [Port Management](#port-management)
  - [Admin Account Creation](#admin-account-creation)
  - [CLI User Management](#cli-user-management)
  - [Starting the Server](#starting-the-server)
- [Debugging](#debugging)
- [Testing](#testing)
- [Updates](#updates)
- [Queue Management](#queue-management)
- [Spam Issues](#spam-issues)
- [OIDC Support](#oidc-support)
- [To-Do](#to-do)
- [References](#references)

## Setup ⚙️

### Fetchmail Issues 📨

Fetchmail might not work properly with large amounts of data. For more information, refer to this [issue](https://github.com/Mailu/Mailu/issues/1719).

#### Deactivating Fetchmail ❌

Before uninstalling Fetchmail, ensure you remove all fetched accounts from the administration panel.

#### Fetchmail Security Concerns 🔐

There are known security concerns with Fetchmail as stated in the [German Wikipedia](https://de.wikipedia.org/wiki/Fetchmail). If you require Fetchmail functions in the future, consider creating a Docker container for [Getmail](https://en.wikipedia.org/wiki/Getmail) as it is considered more secure.

#### Fetchmail Workaround 🔄

If you need to receive emails from another account, follow these steps:

1. Redirect your emails to your new email account.
2. Export all data from your original account.
3. Import all data to your new account.

### Port Management 🌐

Check for any port conflicts and manually change the conflicting ports if necessary. Use the following command to verify:

```bash
netstat -tulpn
```

### Admin Account Creation 👤

To use Mailu, create the primary administrator user account, `admin@{{hostname}}`, using the command below. Replace `PASSWORD` with your preferred password:

```bash
docker-compose -p mailu exec admin flask mailu admin {{admin}} {{hostname}} PASSWORD
```

### CLI User Management 🛠️

For managing users, follow the instructions in the official [Mailu CLI documentation](https://mailu.io/master/cli.html).

### Starting the Server ▶️

To start the server, use the following command:

```bash
docker-compose -p mailu up -d
```

## Debugging 🕵️‍♂️

### Database Access 📂

To access the database, use the following command:

```bash
docker-compose exec -it database mysql -u root -D mailu -p
```

### Container Access 🖥️

To access the front container, use this command:

```bash
docker-compose exec -it front /bin/bash
```

### Restarting Services 🔄

To restart all services, use the following command:

```bash
docker-compose restart
```

### Resending Queued Mails ✉️

To resend queued mails, use this command:

```bash
docker-compose exec -it smtp postqueue -f
```

## Testing 🧪

Use the following tools for testing:

- [SSL-Tools Mailserver Test](https://de.ssl-tools.net/mailservers/)
- [TestEmail.de](http://testemail.de/)

## Updates 🔄

For instructions on updating your Mailu setup, follow the official [Mailu maintenance guide](https://mailu.io/master/maintain.html).

## Queue Management 📬

To manage the Postfix email queue in Mailu, you can use the following commands:

- **Display the email queue**:

  ```bash
  docker compose exec -it smtp postqueue -p
  ```

- **Delete all emails in the queue**:

  ```bash
  docker compose exec -it smtp postsuper -d ALL
  ```

## Spam Issues 🚨

### Inspect 🔎

Use the following tools to monitor your domain and email deliverability:

- [Google Postmaster](https://postmaster.google.com/) - Analyzes deliverability and spam issues for Gmail.
- [Yahoo Postmaster](https://postmaster.yahooinc.com) - Provides insights and delivery reports for Yahoo.
- [mxtoolbox.com](https://mxtoolbox.com)

### Blacklist Check 🚫

If your domain is blacklisted, you can check the status with these services and take steps to remove your domain if necessary:

- [Spamhaus](https://check.spamhaus.org/)
- [Barracuda](https://www.barracudacentral.org/lookups)

### Cloudmark Reset Request 🔄

If your IP or domain is flagged by Cloudmark, you can submit a **reset request**:

- [Cloudmark Reset](https://csi.cloudmark.com/en/reset/)

## OIDC Support 🔐

This role now supports OpenID Connect (OIDC) authentication with [Mailu-OIDC](https://github.com/heviat/Mailu-OIDC)! 🎉

To enable OIDC authentication, simply set the following variable:

```yaml
oidc:
  enabled: true
```

For more details, check out the [Mailu-OIDC repository](https://github.com/heviat/Mailu-OIDC/tree/2024.06).

## References 🔗
- [Mailu compose setup guide](https://mailu.io/1.7/compose/setup.html)
- [SysPass issue #1299](https://github.com/nuxsmin/sysPass/issues/1299)
- [Mailu issue #1719](https://github.com/Mailu/Mailu/issues/1719)
- [Mailu issue #1171](https://github.com/Mailu/Mailu/issues/1171)
- [Mailu issue #2135](https://github.com/Mailu/Mailu/issues/2135)
- [Mailu issue #2827](https://github.com/Mailu/Mailu/issues/2827)
- [Mailu GitHub repository](https://github.com/Mailu/Mailu)
- [Plesk support article on RoundCube connection issue](https://support.plesk.com/hc/en-us/articles/115001264814-Unable-to-log-into-RoundCube-Connection-to-storage-server-failed)
- [Gist by marienfressinaud](https://gist.github.com/marienfressinaud/f284a59b18aad395eb0de2d22836ae6b)

---

For more information about this role, visit the GitHub repositories:
- [Mailu](https://github.com/kevinveenbirkenbach/cymais/tree/master/roles/docker-mailu)
- [Mailu-OIDC](https://github.com/heviat/Mailu-OIDC)

### About this Role ✨

This Mailu Docker role was developed by **[Kevin Veen-Birkenbach](https://veen.world)**.

This `README.md` was optimized with the help of [ChatGPT](https://chat.openai.com)🚀 and this conversations: 

- https://chat.openai.com/share/d1ad5ce7-3aa1-4a14-a959-63393b39374a
- https://chatgpt.com/share/67a4bffb-9330-800f-aed5-715c6a8ced2f