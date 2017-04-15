FROM python:3.6.1-slim
MAINTAINER Anton Berezin <gurunars@gmail.com>

EXPOSE 80

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get -y install apache2 apache2-mpm-worker apache2-threaded-dev libapache2-mod-wsgi-py3 && \
    service apache2 stop | true && \
    a2dissite 000-default.conf | true && \
    a2dissite default-ssl.conf | true

RUN apt-get -y install wget python3-dev apache2-dev && \
    wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.5.15.tar.gz && \
    tar -xzf 4.5.15.tar.gz && \
    cd mod_wsgi-4.5.15 && \
    ./configure --with-python=/usr/local/bin/python3.6 && \
    make install && \
    chmod 644 /usr/lib/apache2/modules/mod_wsgi.so && \
    a2enmod wsgi && \
    apt-get -y remove wget python3-dev apache2-dev && \
    apt-get -y autoremove && \
    rm -rf mod_wsgi-4.5.15 4.5.15.tar.gz

# Defaults

COPY /apache/servername.conf /etc/apache2/sites-available/

RUN a2ensite servername.conf

# For debugs

RUN apt-get -y install less

# DB

RUN apt-get -y install postgresql-client

RUN apt-get -y install wget && \
    cd /usr/bin && \
    wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh && \
    apt-get -y remove wget

# App

RUN mkdir /package
ENV PYTHONPATH /package
WORKDIR /package

COPY /requirements.txt /package/

RUN pip install -r requirements.txt

COPY /apache/app.conf /etc/apache2/sites-available/

RUN a2ensite app.conf

RUN mkdir -p /mount/db && \
    mkdir -p /mount/media

COPY /manage.py /package/
COPY /solarpilot /package/solarpilot
COPY /infographics /package/infographics

ENV DJANGO_SETTINGS_MODULE solarpilot.prod_settings
RUN python manage.py collectstatic --noinput

COPY /docker-start.sh /package/

CMD ["wait-for-it.sh", "postgres:5432", "--", "/bin/bash", "./docker-start.sh"]

