FROM almalinux:9-minimal

LABEL maintainer="anyxel@proton.me"

RUN microdnf install dnf -y
RUN dnf update -y && dnf upgrade -y

# Install Python
RUN dnf install python3.11 -y

# Set python3.11 as python/python3 command
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
RUN echo 2 | update-alternatives --config python3

# Install pip
RUN dnf install python3-pip -y \
    && python3 -m ensurepip --upgrade

# Install git
#RUN dnf install git -y

# Workdir
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# copy project
COPY ./ $APP_HOME

# Install dependencies
RUN cd $APP_HOME \
    && pip install --no-cache-dir -r requirements.txt
