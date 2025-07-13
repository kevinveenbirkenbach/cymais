FROM archlinux:latest

# 1) Update system and install build tools
RUN pacman -Syu --noconfirm \
      git \
      make \
      python \
      python-pip \
      sudo \
    && pacman -Scc --noconfirm

# 2) Define where our venv and repo will live
ENV PKGMGR_VENV=/root/.venvs/pkgmgr
ENV PKGMGR_REPO=/opt/package-manager

# 3) Clone the package-manager sources
RUN git clone https://github.com/kevinveenbirkenbach/package-manager.git $PKGMGR_REPO

# 4) Create the venv and install its Python requirements there
RUN python -m venv $PKGMGR_VENV \
 && $PKGMGR_VENV/bin/pip install --upgrade pip \
 && $PKGMGR_VENV/bin/pip install --no-cache-dir -r $PKGMGR_REPO/requirements.txt

# 5) Write a tiny wrapper so `pkgmgr` always runs inside that venv
RUN printf '#!/bin/sh\n'                                     > /usr/local/bin/pkgmgr \
 && printf '. %s/bin/activate\n' "$PKGMGR_VENV"           >> /usr/local/bin/pkgmgr \
 && printf 'exec python %s/main.py "$@"\n' "$PKGMGR_REPO" >> /usr/local/bin/pkgmgr \
 && chmod +x /usr/local/bin/pkgmgr

# 6) Make sure any scripts in the venv get picked up (if there are any)
ENV PATH="$PKGMGR_VENV/bin:${PATH}"

# 7) Now install CyMaIS via pkgmgr (all inside the venv)
RUN pkgmgr install cymais --clone-mode https

# 8) And ship the container as the cymais CLI
ENTRYPOINT ["cymais"]
CMD ["--help"]
