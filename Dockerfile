FROM archlinux:latest

# 1) Update system and install required tools
RUN pacman -Syu --noconfirm \
    git \
    make \
    python \
    python-pip \
 && pacman -Scc --noconfirm

# 2) Ensure ~/.local/bin is on PATH so pkgmgr & cymais are discoverable
ENV PATH="/root/.local/bin:${PATH}"

# 3) Clone and install Kevin’s Package Manager
RUN git clone https://github.com/kevinveenbirkenbach/package-manager.git /opt/package-manager \
 && cd /opt/package-manager \
 && make setup \
 && ln -s /opt/package-manager/main.py /usr/local/bin/pkgmgr

# 4) Use pkgmgr to install CyMaIS
RUN pkgmgr install cymais

# 5) Default entrypoint to the cymais CLI
ENTRYPOINT ["cymais"]
CMD ["--help"]
