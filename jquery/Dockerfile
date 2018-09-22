FROM node:8.12.0

ENV WORKSPACE /workspace
WORKDIR $WORKSPACE

RUN apt-get update && apt-get install -y --no-install-recommends \
        python-pip \
        chromium \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
    && pip install tox==3.1.2

CMD ["bash"]