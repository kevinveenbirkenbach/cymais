FROM archlinux:latest

# 1) Update system and install build tools + Go for AUR package builds
RUN pacman -Syu --noconfirm \
      base-devel \
      git \
      sudo \
      python \
      python-pip \
      go \
    && pacman -Scc --noconfirm

# 2) Create a non-root user for building AUR packages
RUN useradd -m builder

# 3) Clone & build yay as the unprivileged 'builder' user
USER builder
WORKDIR /home/builder
RUN git clone https://aur.archlinux.org/yay.git \
 && cd yay \
 && makepkg --noconfirm --skippgpcheck

# 4) Switch back to root to install the built yay package system-wide
USER root
RUN pacman -U --noconfirm /home/builder/yay/yay-*.pkg.tar.zst \
 && rm -rf /home/builder/yay

# 5) Define where our pkgmgr virtualenv and repo will live
ENV PKGMGR_VENV=/root/.venvs/pkgmgr
ENV PKGMGR_REPO=/opt/package-manager

# 6) Clone the package-manager sources
RUN git clone https://github.com/kevinveenbirkenbach/package-manager.git $PKGMGR_REPO

# 7) Create the venv and install its Python requirements there
RUN python -m venv $PKGMGR_VENV \
 && $PKGMGR_VENV/bin/pip install --upgrade pip \
 && $PKGMGR_VENV/bin/pip install --no-cache-dir -r $PKGMGR_REPO/requirements.txt

# 8) Write a tiny wrapper so `pkgmgr` always runs inside that venv
RUN printf '#!/bin/sh\n'                                > /usr/local/bin/pkgmgr \
 && printf '. %s/bin/activate\n' "$PKGMGR_VENV"       >> /usr/local/bin/pkgmgr \
 && printf 'exec python %s/main.py "$@"\n' "$PKGMGR_REPO" >> /usr/local/bin/pkgmgr \
 && chmod +x /usr/local/bin/pkgmgr

# 9) Ensure the venv’s bin is first on PATH
ENV PATH="$PKGMGR_VENV/bin:${PATH}"

# 10) Use pkgmgr (inside the venv) to install CyMaIS, allowing AUR dependencies via yay
RUN pkgmgr install cymais --clone-mode https

# 11) Expose the cymais CLI as the container’s entrypoint
ENTRYPOINT ["cymais"]
CMD ["--help"]
