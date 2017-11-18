set -x
docker build -t custom-hello .
docker run --rm custom-hello
docker run --rm custom-hello Docker
docker image rm custom-hello
