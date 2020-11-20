FROM python
COPY . /app
RUN pip install -r /app/requirements.pip

RUN apt update
RUN apt install -y ssh
RUN echo 'Port 2222' >> /etc/ssh/sshd_config

COPY ssh_key.pub /root/.ssh/authorized_keys

EXPOSE 8080 8090 2222
CMD /app/start.sh