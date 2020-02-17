FROM openjdk:15-jdk-buster

WORKDIR /workspace

COPY tox.ini ./
RUN apt-get update && apt-get install -y --no-install-recommends \
        vim \
        python3-pip python3-setuptools python3-wheel \
    && pip3 install tox==3.14.5 \
    && tox --notest --workdir /tmp/tox && rm tox.ini \
    && curl -o /tmp/apache-maven-3.6.3.tgz http://ftp.twaren.net/Unix/Web/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz \
    && tar xf /tmp/apache-maven-3.6.3.tgz -C /usr/local/lib \
    && rm /tmp/apache-maven-3.6.3.tgz \
    && ln -s /usr/local/lib/apache-maven-3.6.3/bin/mvn /usr/local/bin

CMD ["bash"]
