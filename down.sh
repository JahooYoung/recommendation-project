#!/bin/bash

IMAGE_NAME="yjh_rcmd_image"
docker-compose down

if [[ $1 == "clean" ]]; then
    echo "removing image $IMAGE_NAME"
    docker rmi $IMAGE_NAME
fi
