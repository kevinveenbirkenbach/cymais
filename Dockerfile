FROM archlinux:latest

# 1) Update system and install build/runtime deps
RUN pacman -Syu --noconfirm \
      base-devel \
      git \
      python \
      python-pip \
      python-setuptools \
      alsa-lib \
      go \
      rsync \
    && pacman -Scc --noconfirm

# 2) Stub out systemctl & yay so post-install hooks and AUR calls never fail
RUN printf '#!/bin/sh\nexit 0\n' > /usr/bin/systemctl \
    && chmod +x /usr/bin/systemctl \
    && printf '#!/bin/sh\nexit 0\n' > /usr/bin/yay \
    && chmod +x /usr/bin/yay

# 3) Build & install python-simpleaudio from AUR manually (as non-root)
RUN useradd -m builder \
 && su builder -c "git clone https://aur.archlinux.org/python-simpleaudio.git /home/builder/psa && \
                    cd /home/builder/psa && \
                    makepkg --noconfirm --skippgpcheck" \
 && pacman -U --noconfirm /home/builder/psa/*.pkg.tar.zst \
 && rm -rf /home/builder/psa

# 4) Clone Kevin’s Package Manager and create its venv
ENV PKGMGR_REPO=/opt/package-manager \
    PKGMGR_VENV=/root/.venvs/pkgmgr

RUN git clone https://github.com/kevinveenbirkenbach/package-manager.git $PKGMGR_REPO \
 && python -m venv $PKGMGR_VENV \
 && $PKGMGR_VENV/bin/pip install --upgrade pip \
 # install pkgmgr’s own deps + the ansible Python library so cymais import yaml & ansible.plugins.lookup work
 && $PKGMGR_VENV/bin/pip install --no-cache-dir -r $PKGMGR_REPO/requirements.txt ansible \
 # drop a thin wrapper so `pkgmgr` always runs inside that venv
 && printf '#!/bin/sh\n. %s/bin/activate\nexec python %s/main.py "$@"\n' \
           "$PKGMGR_VENV" "$PKGMGR_REPO" > /usr/local/bin/pkgmgr \
 && chmod +x /usr/local/bin/pkgmgr

# 5) Ensure pkgmgr venv bin and user-local bin are on PATH
ENV PATH="$PKGMGR_VENV/bin:/root/.local/bin:${PATH}"

# 6) Copy local CyMaIS source into the image for override
COPY . /opt/cymais-src

# 7) Install CyMaIS via pkgmgr (clone-mode https)
RUN pkgmgr install cymais --clone-mode https

# 8) Override installed CyMaIS with local source and clean ignored files
RUN CMAIS_PATH=$(pkgmgr path cymais) && \
    rm -rf "$CMAIS_PATH"/* && \
    rsync -a --delete --exclude='.git' /opt/cymais-src/ "$CMAIS_PATH"/

# 9) Symlink the cymais script into /usr/local/bin so ENTRYPOINT works
RUN CMAIS_PATH=$(pkgmgr path cymais) && \
    ln -sf "$CMAIS_PATH"/main.py /usr/local/bin/cymais && \
    chmod +x /usr/local/bin/cymais

# 10) Run integration tests
#RUN CMAIS_PATH=$(pkgmgr path cymais) && \
#    cd "$CMAIS_PATH" && \
#    make test

ENTRYPOINT ["cymais"]
CMD ["--help"]
