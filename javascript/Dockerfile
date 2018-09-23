FROM node:8.12.0

ENV WORKSPACE /workspace
WORKDIR $WORKSPACE

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install tox==3.1.2

CMD ["bash"]