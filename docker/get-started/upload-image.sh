docker build -t imsardine/get-started:part-2 .
docker push imsardine/get-started:part-2

docker image rm imsardine/get-started:part-2
docker run -d -p 4000:80 imsardine/get-started:part-2
