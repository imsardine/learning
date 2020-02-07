FROM google/dart:2.7

WORKDIR /workspace

COPY tox.ini ./
RUN apt-get update && apt-get install -y --no-install-recommends \
        vim \
        python3-pip \
    && pip3 install tox==3.14.3 \
    && tox --notest --workdir /tmp/tox && rm tox.ini

CMD ["bash"]
