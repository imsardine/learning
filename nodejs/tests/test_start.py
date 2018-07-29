import pytest

DOCKER_RUN = 'docker run --rm -v $PWD:/usr/src/app -w /usr/src/app node:$NODE_VERSION node %s'

def test_hello_world(workspace):
    workspace.src('index.js', """
    console.log('Hello, World!');
    """)

    assert workspace.run(DOCKER_RUN % 'index.js').out == 'Hello, World!\n'
