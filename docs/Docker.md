# Docker Build Guide 🚢

This guide explains how to build the **CyMaIS** Docker image with advanced options to avoid common issues (e.g. mirror timeouts) and control build caching.

---

## 1. Enable BuildKit (Optional but Recommended)

Modern versions of Docker support **BuildKit**, which speeds up build processes and offers better caching.

```bash
# On your host, enable BuildKit for the current shell session:
export DOCKER_BUILDKIT=1
```

> **Note:** You only need to set this once per terminal session.

---

## 2. Build Arguments Explained

When you encounter errors like:

```text
:: Synchronizing package databases...
error: failed retrieving file 'core.db' from geo.mirror.pkgbuild.com : Connection timed out after 10002 milliseconds
error: failed to synchronize all databases (failed to retrieve some files)
```

it usually means the default container network cannot reach certain Arch Linux mirrors. To work around this, use:

* `--network=host`
  Routes all build-time network traffic through your host’s network stack.

* `--no-cache`
  Forces a fresh build of every layer by ignoring Docker’s layer cache. Useful if you suspect stale cache entries.

---

## 3. Recommended Build Command

```bash
# 1. (Optional) Enable BuildKit
export DOCKER_BUILDKIT=1

# 2. Build with host networking and no cache
docker build \
  --network=host \
  --no-cache \
  -t cymais:latest \
  .
```

**Flags:**

* `--network=host`
  Ensures all `pacman -Syu` and other network calls hit your host network directly—eliminating mirror connection timeouts.

* `--no-cache`
  Guarantees that changes to package lists or dependencies are picked up immediately by rebuilding every layer.

* `-t cymais:latest`
  Tags the resulting image as `cymais:latest`.

---

## 4. Running the Container

Once built, you can run CyMaIS as usual:

```bash
docker run --rm -it \
  -v "$(pwd)":/opt/cymais \
  -w /opt/cymais \
  cymais:latest cymais --help
```

Mount any host directory into `/opt/cymais/logs` to persist logs across runs.

---

## 5. Further Troubleshooting

* **Mirror selection:** If you still see slow or unreachable mirrors, consider customizing `/etc/pacman.d/mirrorlist` in a local Docker stage or on your host to prioritize faster mirrors.

* **Firewall or VPN:** Ensure your host’s firewall or VPN allows outgoing connections on port 443/80 to Arch mirror servers.

* **Docker daemon config:** On some networks, you may need to configure Docker’s daemon proxy settings under `/etc/docker/daemon.json`.

## 6. Live Development via Volume Mount

The CyMaIS installation inside the container always resides at:

```
/root/Repositories/github.com/kevinveenbirkenbach/cymais
```

To apply code changes without rebuilding the image, mount your local installation directory into that static path:

```bash
# 1. Determine the CyMaIS install path on your host
CMAIS_PATH=$(pkgmgr path cymais)

# 2. Launch the container with a bind mount:
docker run --rm -it \
  -v "${CMAIS_PATH}:/root/Repositories/github.com/kevinveenbirkenbach/cymais" \
  -w "/root/Repositories/github.com/kevinveenbirkenbach/cymais" \
  cymais:latest cymais make build
```

Or, to test the CLI help interactively:

```bash
docker run --rm -it \
  -v "${CMAIS_PATH}:/root/Repositories/github.com/kevinveenbirkenbach/cymais" \
  -w "/root/Repositories/github.com/kevinveenbirkenbach/cymais" \
  cymais:latest --help
```

Any edits you make in `${CMAIS_PATH}` on your host are immediately reflected inside the container, eliminating the need for repeated `docker build` cycles.

---

With these options, your Docker builds should complete reliably, even in restrictive network environments. Happy building! 🚀
