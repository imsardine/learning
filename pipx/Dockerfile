FROM python:3.13.0

WORKDIR /workspace
ENV PATH $PATH:/root/.local/bin

COPY tox.ini ./
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install pipx==1.7.1 \
    && pip install tox==4.16.0 \
    && tox --notest --workdir /tmp/tox && rm tox.ini

CMD ["bash"]
