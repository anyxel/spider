FROM almalinux:latest

LABEL maintainer="anyxel@proton.me"

RUN dnf update -y && dnf upgrade -y

# Install necessay tools
RUN dnf install yum-utils -y \
    && dnf install epel-release -y \
    && dnf install gcc make -y

# Install Python
RUN dnf install python3.11 -y

# Set python3.11 as default python3 command
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
RUN echo 2 | update-alternatives --config python3

# Set python3 as python command
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install pip
RUN dnf install python3-pip -y \
    && python3 -m ensurepip --upgrade

# Install sqlite
RUN dnf install sqlite -y && sqlite3 db.sqlite3 ""

RUN pip install daphne

# Workdir
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# copy project
COPY ./ $APP_HOME

# Install dependencies
RUN cd $APP_HOME \
    && pip install --no-cache-dir -r requirements.txt

# Extra
RUN chmod +x *.sh
