FROM dokken/ubuntu-22.04
MAINTAINER Tangent Tech <info@tangenttek.com>

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8

#Copy the odoo files
RUN mkdir /opt/odoo16ce
RUN mkdir /opt/odoo16ce/core
RUN mkdir /opt/odoo16ce/custom
RUN mkdir /opt/odoo16ce/custom_odoo_module
RUN mkdir /etc/odoo

COPY ./core /opt/odoo16ce/core
COPY ./custom /opt/odoo16ce/custom
COPY ./custom_odoo_module /opt/odoo16ce/custom_odoo_module

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/


RUN apt-get update
RUN apt-get upgrade -y

# create user that will be used to run system by name odoo
RUN adduser --system --home=/opt/odoo --group odoo

RUN apt-get -y install build-essential  \
    wget git python3-pip  \
    python3-dev python3-venv  \
    python3-wheel libfreetype6-dev  \
    libxml2-dev libzip-dev libsasl2-dev  \
    python3-setuptools libjpeg-dev  \
    zlib1g-dev libpq-dev libxslt1-dev  \
    libldap2-dev libtiff5-dev  \
    libopenjp2-7-dev \
    nano \
    libffi-dev

# install wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb

COPY ./wkhtmltopdf-installation.sh /

RUN chmod +x /wkhtmltopdf-installation.sh

RUN /wkhtmltopdf-installation.sh
#RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
#
#RUN dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
#
#RUN apt --fix-broken install

    #    wkhtmltopdf
#RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
#RUN sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
#RUN sudo apt install -f

# install latest postgresql-client
RUN apt-get install -y postgresql-client

#
RUN pip3 install wheel
RUN pip3 install --upgrade pip
#
#COPY ./core/requirements.txt /opt/odoo16ce/core/requirements.txt

RUN pip3 install -r /opt/odoo16ce/core/requirements.txt

#RUN apt-get install -y libssl-dev libpq-dev


# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons for all
RUN chown odoo:odoo -R /etc/odoo \
    && mkdir -p /mnt/extra-addons \
    && chown -R odoo /mnt/extra-addons \
    && chown odoo:odoo /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && mkdir -p /opt/odoo/data_dir \
    && chown -R odoo:odoo /opt/odoo/data_dir \
    && mkdir -p /opt/odoo/logs \
    && chown -R odoo:odoo /opt/odoo/logs \
    && mkdir -p /opt/backups \
    && chown -R odoo:odoo /opt/backups \
    && chown -R odoo:odoo /opt/odoo16ce \
    && chown -R odoo:odoo /opt/odoo16ce/custom \
    && chown -R odoo:odoo /opt/odoo16ce/custom_odoo_module

# volumes are managed in composer file
#VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Expose Odoo services
EXPOSE 8069

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

# Set default user when running the container
USER odoo

#ENTRYPOINT ["/entrypoint.sh"]
CMD ["/entrypoint.sh","-g","daemon off"]