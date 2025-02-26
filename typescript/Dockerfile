FROM node:20.15.1

WORKDIR /workspace
ENV PATH $PATH:/root/.local/bin

COPY tox.ini ./
RUN apt-get update && apt-get install -y --no-install-recommends \
        tree \
        vim \
        python3 \
        pipx \
    && npm install -g typescript@5.5.4 \
    && pipx install tox==4.16.0 \
    && tox --notest --workdir /tmp/tox && rm tox.ini

CMD ["bash"]
