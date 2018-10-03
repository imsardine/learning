FROM python:3.7.0

ENV WORKSPACE /workspace
WORKDIR $WORKSPACE

RUN apt-get update && apt-get install -y --no-install-recommends \
       vim \
       jq \
    && pip install tox==3.1.2

CMD ["bash"]