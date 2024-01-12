FROM almalinux:9-minimal

LABEL maintainer="anyxel@proton.me"

RUN microdnf install dnf -y
RUN dnf update -y
RUN dnf upgrade -y

# Install extra packages
RUN dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm -y
RUN dnf install https://rpms.remirepo.net/enterprise/remi-release-9.rpm -y
RUN dnf install which -y

# Install Python
RUN dnf install python3.11 -y

# Set python3.11 as python/python3 command
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
RUN echo 2 | update-alternatives --config python3

# Install pip
RUN dnf install python3-pip -y \
    && python3 -m ensurepip --upgrade

# Workdir
ENV APP_HOME=/var/www/html
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# copy project
COPY ./ $APP_HOME

# Install dependencies
RUN cd $APP_HOME \
    && pip install -r requirements.txt

# tools
RUN dnf install nmap -y
