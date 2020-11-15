#!/bin/bash

IMAGE_NAME="yjh_rcmd_image"
echo "building image ${IMAGE_NAME}"
docker build -t="${IMAGE_NAME}" .

docker-compose up -d

# echo "wait 6s"
# sleep 6

docker exec node2 start-zookeeper.sh
docker exec node3 start-zookeeper.sh
docker exec node4 start-zookeeper.sh

docker exec node3 start-apache-mongo.sh
docker exec node3 start-yarn.sh  # special handle for yarn
docker exec node4 start-apache-mongo.sh
docker exec node1 start-apache-mongo.sh
docker exec node2 start-apache-mongo.sh

docker exec node1 start-web.sh
