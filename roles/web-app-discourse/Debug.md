## Discourse Debugging Guide for Docker Role

This document explains how to locate and use key log file paths on both the host and inside the container for a Docker-based Discourse installation deployed via the `web-app-discourse` role.

### 1. Host Paths

Discourse log files are stored in the Docker volume named `discourse_data`. On the host, you can find them at:

* **Rails Production Log**:

  ```bash
  cat /var/lib/docker/volumes/discourse_data/_data/log/rails/production.log | grep -i mail
  ```

  Filters for email-related entries:

  * **Queued emails**: `Email::Sender: queued mail to user@example.com`
  * **Errors**: e.g. `Net::SMTPAuthenticationError`, `SMTPConnectionError`

* **Sidekiq Log**:

  ```bash
  cat /var/lib/docker/volumes/discourse_data/_data/log/sidekiq.log | grep -i mail
  ```

  Shows asynchronous mail job executions, retries, and failures.

### 2. Inside the Container

To inspect logs within the container, enter it:

```bash
cd /var/discourse
./launcher enter app
```

Logs are mounted under `/var/log` inside the container:

* **Rails Production Log**:

  ```bash
  tail -n 200 /var/log/rails/production.log | grep -i mail
  ```

  * **Info**: `I, [timestamp] INFO -- : Email::Sender: queued mail to ...`
  * **Error**: `E, [timestamp] ERROR -- : Net::SMTPSyntaxError ...`

* **Sidekiq Log**:

  ```bash
  tail -n 200 /var/log/sidekiq.log | grep -i mail
  ```

  * **Execution**: `Mail::MessageJob JID-...`
  * **Retries/Exceptions** on delivery failure.

### 3. Live Streaming Logs

For real-time monitoring while reproducing an issue:

```bash
# On host:

tail -f \
  /var/lib/docker/volumes/discourse_data/_data/log/rails/production.log \
  /var/lib/docker/volumes/discourse_data/_data/log/sidekiq.log | grep -i mail

# Or inside container:
tail -f /var/log/rails/production.log /var/log/sidekiq.log | grep -i mail
```

### 4. Enabling Verbose Email Debugging

For detailed SMTP conversation logging:

```bash
# Inside container
rails c
> Discourse.debug_email = true
```

Send a test email:

```bash
rails c
> UserMailer.test_email("you@example.com").deliver_now
```

Then check logs for the full SMTP handshake details.

### 5. Flushing Redis Cache

After configuration changes, clear Redis to remove stale session or cached data:

```bash
# Inside container
rails r "Redis.new.flushall"
```

### 6. Sidekiq Web UI

In the Admin UI under **Plugins → Sidekiq**, monitor queues, retries, and failed jobs for additional context.

---

Use this guide to quickly locate and interpret Discourse logs on both host and container, enabling efficient debugging of email delivery and background job issues in a Docker deployment managed by the `web-app-discourse` role.
