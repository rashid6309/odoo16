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

COPY ./core /opt/odoo16ce/core
COPY ./custom /opt/odoo16ce/custom
COPY ./custom_odoo_module /opt/odoo16ce/custom_odoo_module

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY odoo.conf /etc/odoo/


# create user that will be used to run system by name odoo
RUN adduser --system --home=/opt/odoo16ce --group odoo

RUN apt-get update
#RUN apt-get upgrade


RUN apt-get -y install build-essential  \
    wget git python3-pip  \
    python3-dev python3-venv  \
    python3-wheel libfreetype6-dev  \
    libxml2-dev libzip-dev libsasl2-dev  \
    python3-setuptools libjpeg-dev  \
    zlib1g-dev libpq-dev libxslt1-dev  \
    libldap2-dev libtiff5-dev  \
    libopenjp2-7-dev \
    && apt-get -y install wkhtmltopdf
#
RUN pip3 install wheel
#
COPY ./core/requirements.txt /opt/odoo16ce/core/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/odoo16ce/core/requirements.txt

RUN #apt-get install -y libssl-dev libpq-dev

RUN apt install -y nano
# install latest postgresql-client
RUN apt-get install -y postgresql-client

# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN chown odoo /etc/odoo/odoo.conf \
    && mkdir -p /mnt/extra-addons \
    && mkdir -p /var/lib/odoo \
    && chown -R odoo /mnt/extra-addons

#VOLUME ["./",""]

RUN mkdir -p /var/lib/odoo \
    && chown -R odoo /var/lib/odoo \
    && chown odoo /entrypoint.sh
# Expose Odoo services
EXPOSE 8069

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

#COPY ./wait-for-psql.py /usr/local/bin/wait-for-psql.py

# Set default user when running the container
USER odoo

#ENTRYPOINT ["/entrypoint.sh"]
CMD ["/entrypoint.sh","-g","daemon off"]