FROM wordpress

# Update and installation of msmtp
RUN apt-get update && \
    apt-get install -y msmtp msmtp-mta && \
    rm -rf /var/lib/apt/lists/*

# Copy the msmtp configuration into the container
COPY config/msmtprc.conf /etc/msmtprc

# Copy the PHP configuration for uploads (and mail settings)
COPY upload.ini $PHP_INI_DIR/conf.d/