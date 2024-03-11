FROM ubuntu:latest
LABEL maintainer="anyxel@proton.me"

# Install necessay tools
RUN apt update --fix-missing \
    && apt install -y software-properties-common \
    && apt install -y tcl \
    && add-apt-repository -y ppa:deadsnakes/ppa

# Install more tools
RUN apt install wget unzip unzip -y

# Install Python
RUN apt install python3.11 -y

# Set python3.11 as default python3 command
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --config python3

# Set python3.11 as python command
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Install pip & upgrade
RUN apt install python3-pip -y && pip3 --no-cache-dir install --upgrade pip

# Install python servers
RUN pip install daphne \
    && pip install tornado

# Install sqlite
RUN apt install sqlite -y && sqlite3 db.sqlite3 ""

# Supervisor
RUN apt install supervisor -y
COPY ./.docker/prod/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Workdir
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Copy project && install dependencies
COPY .. $APP_HOME
RUN cd $APP_HOME && pip install --no-cache-dir -r requirements.txt

# Extra
RUN chmod +x *.sh
RUN chmod +x terminal.py
RUN find core/scripts -type f -exec chmod +x {} \;
RUN find tools/scripts -type f -exec chmod +x {} \;

# Run
CMD ["/usr/bin/supervisord"]
