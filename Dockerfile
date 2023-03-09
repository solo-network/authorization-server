FROM python:3.10.2-slim
RUN echo "America/Sao_Paulo" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get -y update
RUN apt-get install -y apt-utils build-essential gcc
RUN apt-get -y install git
RUN apt-get -y install --no-install-recommends default-jre
RUN apt-get -y install openjdk-11-jdk
RUN useradd -ms /bin/bash python
RUN apt install libnss3-tools -y
RUN apt install sqlite3 -y
RUN apt install wget -y
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64
RUN cp mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert
RUN chmod +x /usr/local/bin/mkcert
RUN mkcert -install
RUN mkcert -cert-file cert.pem -key-file /key.pem localhost 127.0.0.1
RUN chmod 755 cert.pem
RUN chmod 755 key.pem
RUN pip install pdm

USER python
WORKDIR /home/python/app

ENV MY_PYTHON_PACKAGES=/home/python/app/__pypackages__/3.10
ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH $PATH:${MY_PYTHON_PACKAGES}/bin

RUN echo 'eval "$(pdm --pep582)"' >> ~/.bashrc

RUN export JAVA_HOME
RUN export PATH=$PATH:$JAVA_HOME



CMD [ "tail", "-f", "/dev/null" ]